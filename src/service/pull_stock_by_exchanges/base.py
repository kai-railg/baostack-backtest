# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/04 13:50:59
@Author  :   kai.wang@westwell-lab.com 
'''
import typing
from abc import abstractmethod
import requests
import xlrd

from src.setting import logger
from src.schema import StockInfoSchema


class PullExchangesStockBase(object):
    def __init__(self) -> None:
        self.request_url = ""
        self.file_path = ""

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

    def get_stock_info(self) -> typing.Generator:
        """
        获取股票信息
        """
        resp = self.request_exchanges_all_stock()

        self.write_stock_to_file(resp)
        for row in self.read_stock_file():
            yield self.load_stock_info(row)
