# -*- coding: utf-8 -*-
from base64 import b64encode
from datetime import datetime
from hashlib import sha1
from hmac import new as hmac
from typing import Optional
from urllib.parse import urlencode, quote_plus, quote
from uuid import uuid4

import httpx
from loguru import logger

from .base import BaseDnsProvider


class AliDnsProvider(BaseDnsProvider):
    """阿里DNS

    参考: https://github.com/NewFuture/DDNS/blob/master/dns/alidns.py
    """

    ENDPOINT = "https://alidns.aliyuncs.com/"

    def __init__(self, config: dict):
        super().__init__(config)

        assert "access_key_id" in config, KeyError("阿里云DNS配置缺少access_key_id")
        self.access_key_id: str = self.config["access_key_id"]

        assert "access_key_secret" in config, KeyError(
            "阿里云DNS配置缺少access_key_secret"
        )
        self.access_key_secret: str = self.config["access_key_secret"]

    def sign_params(self, params: dict, method: str = "POST"):
        """签名参数"""

        _params = params.copy()
        _params.update(
            {
                "Format": "json",
                "Version": "2015-01-09",
                "AccessKeyId": self.access_key_id,
                "Timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "SignatureMethod": "HMAC-SHA1",
                "SignatureNonce": uuid4().hex,
                "SignatureVersion": "1.0",
            }
        )
        query = urlencode(sorted(_params.items()))
        query = query.replace("+", "%20")
        sign = method + "&" + quote_plus("/") + "&" + quote(query, safe="")

        sign = hmac(
            (self.access_key_secret + "&").encode("utf-8"), sign.encode("utf-8"), sha1
        ).digest()
        sign = b64encode(sign).decode("utf-8").strip()
        _params["Signature"] = sign
        return _params

    def request(self, params: dict):
        """API请求"""

        params = {k: v for k, v in params.items() if v is not None}
        params = self.sign_params(params)
        logger.debug(params)

        resp = httpx.post(self.ENDPOINT, data=params)
        status_code = resp.status_code
        if status_code < 200 or status_code >= 300:
            raise Exception(
                f"阿里云DNS请求失败, status_code: {status_code}, text: {resp.text}"
            )
        else:
            return resp.json()

    def get_domain_info(self, domain: str):
        """切割域名获取主域名和对应ID"""

        data = self.request({"Action": "GetMainDomainName", "InputString": domain})
        rr = data["RR"]
        domain_name = data["DomainName"]
        return rr, domain_name

    def get_record(
        self, domain_name: str, rr: Optional[str] = None, line: str = "default"
    ):
        """获取已有记录"""

        data = self.request(
            {
                "Action": "DescribeDomainRecords",
                "DomainName": domain_name,
                "RRKeyWord": rr,
                "Line": line,
                "PageSize": 100,
            }
        )
        for record in data["DomainRecords"]["Record"]:
            if record["RR"] == rr and record["Line"] == line:
                return record
        return None

    def set_dns_record(self, domain: str, value: str, type: str = "A", **kwargs):
        """设置DNS记录"""

        line = kwargs.get("line", "default")  # 解析线路
        ttl = kwargs.get("ttl")  # TTL

        rr, domain_name = self.get_domain_info(domain)
        record = self.get_record(domain_name, rr, line)

        if record:  # 记录已存在
            if record["Type"] == type and record["Value"] == value:
                logger.info(f"{domain} 已经解析为 {value}, 无需更新")
                return
            self.request(
                {
                    "Action": "UpdateDomainRecord",
                    "RecordId": record["RecordId"],
                    "RR": rr,
                    "Type": type,
                    "Value": value,
                    "TTL": ttl,
                }
            )
        else:
            self.request(
                {
                    "Action": "AddDomainRecord",
                    "DomainName": domain_name,
                    "RR": rr,
                    "Type": type,
                    "Value": value,
                    "TTL": ttl,
                    "Line": line,
                }
            )
