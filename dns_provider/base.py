# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class BaseDnsProvider(ABC):
    """DNS提供商基类"""

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def set_dns_record(self, domain: str, value: str, type: str = "A", **kwargs):
        pass
