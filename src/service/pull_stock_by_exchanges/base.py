# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/04 13:50:59
@Author  :   kai.wang@westwell-lab.com 
'''
import os
import time
import json
import typing
from abc import abstractmethod

import requests

from src.setting import logger
from src.schema import StockInfoSchema


class PullExchangesStockBase(object):
    def __init__(self) -> None:
        self.request_url = ""
        self.file_path = ""
        self.cache_file_path = "./src/static/STOCK_CACHE_DATE_FILE.json"
        self.exchanges_name = ""

    @abstractmethod
    def request_exchanges_all_stock(self) -> requests.Response:
        """
        请求交易所股票列表
        """
        raise

    def write_stock_to_file(self, resp: requests.Response) -> None:
        """
        将请求到的股票列表写入文件
        """
        with open(self.file_path, 'wb') as file:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        # 写入到缓存文件
        stock_date_map = self.autoread_json_file(self.cache_file_path)
        stock_date_map[self.exchanges_name] = time.time()
        with open(self.cache_file_path, 'w') as f:
            json.dump(stock_date_map, f, indent=4)

    @abstractmethod
    def read_stock_file(self) -> typing.Generator:
        """
        读取股票列表文件
        """
        raise

    @abstractmethod
    def load_stock_info(self, stock_info_row: typing.List) -> StockInfoSchema:
        """
        反序列化股票信息
        """
        raise

    def autoread_json_file(self, path: str, default: typing.Callable = None) -> typing.Any | dict:
        if not os.path.exists(path):
            return default and default() or {}
        with open(path, "r") as f:
            return json.load(f)

    def is_cache(self) -> bool:
        if not os.path.exists(self.file_path):
            return False
        stock_date_map: dict = self.autoread_json_file(self.cache_file_path)
        date = stock_date_map.get(self.exchanges_name, 0)
        # 15天
        if time.time() - date > 15 * 60 * 60 * 24:
            return False
        return True

    def get_stock_info(self) -> typing.Generator:
        """
        获取股票信息
        """
        if self.is_cache() is False:
            resp = self.request_exchanges_all_stock()
            self.write_stock_to_file(resp)

        for row in self.read_stock_file():
            yield self.load_stock_info(row)
