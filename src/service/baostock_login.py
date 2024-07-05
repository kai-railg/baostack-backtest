# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/03 14:14:41
@Author  :   kai.wang@westwell-lab.com 
'''

from os import error
from typing import Any, Generator
import baostock as bs
from baostock.data.resultset import ResultData
from contextlib import contextmanager

from src.setting import logger

__all__ = ["baostock_login"]

@contextmanager
def baostock_login() -> Generator:
    """
    baostock 登录
    """
    lg = bs.login()
    logger.debug(f"Login respond error_code: {lg.error_code}, error_msg: {lg.error_msg}")
    yield lg
    bs.logout()