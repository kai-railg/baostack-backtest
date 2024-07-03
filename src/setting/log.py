# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/03 14:40:09
@Author  :   kai.wang@westwell-lab.com 
'''

import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time

from src.setting.settings import LOGGER_LEVEL


def setup_logger(name: str):
    # 创建一个 logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOGGER_LEVEL))  # 设置最低日志等级

    # 创建日志文件名
    log_filename = f"./log/{name}.log"

    # 创建一个 handler，用于写入日志文件，每天滚动一次日志文件
    handler = TimedRotatingFileHandler(
        log_filename,
        when="midnight",
        interval=1,
        backupCount=90,  # 保留90天的日志
        encoding='utf-8'
    )

    # 设置本地时区
    handler.suffix = "%Y-%m-%d"
    handler.namer = lambda x: x.split(".")[0] + handler.suffix

    # 创建日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 添加日志格式到 handler
    handler.setFormatter(formatter)

    # 添加 handler 到 logger
    logger.addHandler(handler)

    return logger


logger = setup_logger("backtest")
