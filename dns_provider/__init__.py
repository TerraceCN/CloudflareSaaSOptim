# -*- coding: utf-8 -*-
from .alidns import AliDnsProvider
from .base import BaseDnsProvider

DNS_PROVIDER = {
    "alidns": AliDnsProvider,
}

__all__ = ["BaseDnsProvider", "DNS_PROVIDER"]
