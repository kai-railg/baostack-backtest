# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/04 10:26:05
@Author  :   kai.wang@westwell-lab.com 
'''
import typing

import requests
import xlrd

from src.schema import StockInfoSchema, ExchangesEnum
from src.setting import logger, SH_ALL_STOCK_URL
from .base import PullExchangesStockBase


class PullSHStock(PullExchangesStockBase):
    """
    上交所股票列表详情页
    http://www.sse.com.cn/assortment/stock/list/share/
    """
    def __init__(self) -> None:
        super().__init__()
        self.request_url = SH_ALL_STOCK_URL or "http://query.sse.com.cn/sseQuery/commonExcelDd.do?sqlId=COMMON_SSE_CP_GPJCTPZ_GPLB_GP_L&type=inParams&CSRC_CODE=&STOCK_CODE=&REG_PROVINCE=&STOCK_TYPE=1&COMPANY_STATUS=2,4,5,7,8"
        self.file_path = "./src/static/SH_STOCK_LIST.xls"

    def request_exchanges_all_stock(self) -> requests.Response:

        resp = requests.post(self.request_url, headers={
            "Accept-Encoding": "gzip, deflate, br",
            # "Host": "prod-ua.sseinfo.com",
            "Referer": "http://www.sse.com.cn/",
            "Origin": "http://www.sse.com.cn",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        })
        if resp.status_code != 200:
            raise Exception(f"上交所股票列表请求失败, {resp.status_code, resp.text}")
        return resp

    def read_stock_file(self) -> typing.Generator:

        workbook: xlrd.Book = xlrd.open_workbook(self.file_path)

        # 获取第一个工作表
        sheet = workbook.sheet_by_index(0)

        # 遍历工作表中的每一行和每一列
        for row_idx in range(sheet.nrows):
            if row_idx == 0:
                continue
            yield sheet.row_values(row_idx)

    def load_stock_info(self, stock_info_row: typing.List) -> StockInfoSchema:
        # A股代码	B股代码	证券简称	扩位证券简称	公司英文全称	上市日期
        code, b_code, name, name_alias, name_english, appear_time = stock_info_row
        return StockInfoSchema(code=code, name=name, exchanges_alias=ExchangesEnum.sh, appear_time=appear_time)
