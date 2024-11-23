# -*- coding: utf-8 -*-
from typing import Any

import toml

with open("config.toml", "r", encoding="utf-8") as fp:
    CONFIG: dict = toml.load(fp)

CONFIG_CLOUDFLARE_ST: dict[str, Any] = CONFIG.get("cloudflare_st", {})

CONFIG_DNS_PROVIDER: dict[str, dict] = CONFIG.get("dns_provider", {})

CONFIG_DNS: list[dict[str, Any]] = CONFIG.get("dns", [])

__all__ = [
    "CONFIG",
    "CONFIG_CLOUDFLARE_ST",
    "CONFIG_DNS_PROVIDER",
    "CONFIG_DNS",
]
