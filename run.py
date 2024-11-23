# -*- coding: utf-8 -*-
import csv
from functools import cache

from loguru import logger

from config import config
from dns_provider import BaseDnsProvider, DNS_PROVIDER


def read_cloudflare_st_result(result_file: str = "result.csv") -> list:
    """读取CloudflareSpeedtest结果"""

    try:
        with open(result_file, "r", encoding="utf-8") as fp:
            reader = csv.DictReader(fp)
            return [row for row in reader]
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到CloudflareSpeedtest结果文件: {result_file}")


@cache
def get_dns_provider(provider: str) -> BaseDnsProvider:
    """获取DNS服务商对象"""

    if provider not in DNS_PROVIDER:
        raise KeyError(f"不支持的DNS服务商: {provider}")

    dns_provider_configs: dict[str, dict] = config.get("dns_provider", {})
    dns_provider_config = dns_provider_configs.get(provider, {})
    dns_provider = DNS_PROVIDER[provider](dns_provider_config)
    return dns_provider


def set_dns_record(dns_provider: BaseDnsProvider, dns: dict, ip: str):
    """设置DNS记录"""

    if "domain" not in dns:
        logger.error(f"未指定DNS域名: {dns}")
        return

    dns_provider.set_dns_record(value=ip, **dns)


def main():
    cloudflare_speed_test_config = config.get("cloudflare_speed_test_config", {})
    result_file = cloudflare_speed_test_config.get("result_file", "result.csv")
    results = read_cloudflare_st_result(result_file)

    if len(results) == 0:
        logger.error("测速结果为空")
        exit(1)
    result = results[0]
    logger.info(
        f"使用IP: {result['IP 地址']}, 丢包率: {result['丢包率']}, 平均延迟: {result['平均延迟']}, 下载速度 (MB/s): {result['下载速度 (MB/s)']}"
    )

    dns: dict
    for dns in config.get("dns", []):
        if "provider" not in dns:
            logger.error(f"未指定DNS服务商: {dns}")
            continue
        provider = dns["provider"]

        dns_provider = get_dns_provider(provider)

        try:
            set_dns_record(dns_provider, dns, result["IP 地址"])
            logger.info(f"设置DNS记录成功: {dns}")
        except Exception:
            logger.exception(f"设置DNS记录失败: {dns}")


if __name__ == "__main__":
    main()
