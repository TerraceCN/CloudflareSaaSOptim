# -*- coding: utf-8 -*-
import toml

with open("config.toml", "r", encoding="utf-8") as fp:
    config: dict = toml.load(fp)

__all__ = ["config"]
