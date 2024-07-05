# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/04 10:42:01
@Author  :   kai.wang@westwell-lab.com 
'''
import typing

import requests
import openpyxl

from src.setting import logger, SZ_ALL_STOCK_URL
from src.schema import StockInfoSchema, ExchangesEnum
from .base import PullExchangesStockBase


class PullSZStock(PullExchangesStockBase):
    """
    深交所股票列表详情页
    http://www.szse.cn/market/product/stock/list/index.html
    """
    def __init__(self) -> None:
        super().__init__()
        self.request_url = SZ_ALL_STOCK_URL or "http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1110&TABKEY=tab1&random=0.7730754472207189"
        self.file_path = "./src/static/SZ_STOCK_LIST.xlsx"

    def request_exchanges_all_stock(self) -> requests.Response:
        resp = requests.get(self.request_url, headers={
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.szse.cn",
            "Referer": "http://www.szse.cn/market/product/stock/list/index.html",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        })
        if resp.status_code != 200:
            raise Exception("深交所股票列表请求失败")
        return resp

    def read_stock_file(self) -> typing.Generator:

        workbook = openpyxl.load_workbook(self.file_path)

        # 获取第一个工作表
        sheet = workbook.active

        # 遍历工作表中的每一行和每一列
        for row in sheet.iter_rows(min_row=2, values_only=True):
            yield row


    def load_stock_info(self, stock_info_row: typing.List) -> StockInfoSchema:
        # ('板块', '公司全称', '英文名称', '注册地址', 'A股代码', 'A股简称', 'A股上市日期', 'A股总股本', 'A股流通股本', 'B股代码', 'B股 简 称', 'B股上市日期', 'B股总股本', 'B股流通股本', '地      区', '省    份', '城     市', '所属行业', '公司网址', '未盈利', '具有表决权差异安排', '具有协议控制架构')
        # market, company_name, english_name, register_address, a_code, a_name, a_appear_time, a_total_capital, a_circulation_capital, b_code, b_name, b_appear_time, b_total_capital, b_circulation_capital, area, province, city, industry, website, no_profit, vote_differ_arrange, protocol_control_architecture
        market, company_name, english_name, register_address, a_code, a_name, a_appear_time, a_total_capital, a_circulation_capital, b_code, b_name, b_appear_time, b_total_capital, b_circulation_capital, area, province, city, industry, website, no_profit, vote_differ_arrange, protocol_control_architecture = stock_info_row
        return StockInfoSchema(
            code=a_code, name=a_name, 
            exchanges_alias=ExchangesEnum.sz, 
            appear_time=a_appear_time.replace("-", ""),
            english_name=english_name,
            company_name=company_name,
            register_address=register_address,
            total_capital=a_total_capital,
            circulation_capital=a_circulation_capital,
            website=website,
            no_profit=no_profit,
            vote_differ_arrange=vote_differ_arrange,
            protocol_control_architecture=protocol_control_architecture,
        )
