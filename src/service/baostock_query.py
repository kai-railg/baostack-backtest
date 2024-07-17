# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/03 14:19:21
@Author  :   kai.wang@westwell-lab.com 
'''
from typing import Any, Generator, List
from datetime import datetime


import baostock as bs
import pandas as pd
from baostock.data.resultset import ResultData

from src.setting import logger
from src.schema import StockInfoSchema, StockTradeInfoSchema

__all__ = ["bsq"]


class BaoStockQuery(object):
    def __init__(self) -> None:
        pass
    @property
    def _default_fields(self):
        return "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"

    def _load_row_data(self, rs: ResultData) -> Generator:
        while (rs.error_code == '0') & rs.next():
            row_dict = {
                field: field_val for field,
                field_val in zip(rs.fields, rs.get_row_data())
            }
            # 过滤 st股票, 停牌股票
            print(row_dict)
            if (
                row_dict["isST"] == "1") or (
                row_dict["tradestatus"] == "0"
            ):
                continue
            yield StockTradeInfoSchema(**row_dict)

    @property
    def _get_current_time(self) -> str:
        return f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"

    def query_k_data_plus(self, stock: StockInfoSchema, adjustflag=2, frequency="d") -> Generator:
        """
        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数,参见“历史行情指标参数”章节;“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标:date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标:date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        # adjustflag 1:后复权, 2:前复权, 0:不复权
        # frequency 默认为d,日k线;d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据,不区分大小写;指数没有分钟线数据;周线每周最后一个交易日才可以获取,月线每月最后一个交易日才可以获取。
        # 股票停牌时,对于日线,开、高、低、收价都相同,且都为前一交易日的收盘价,成交量、成交额为0,换手率为空。
        """
        rs: ResultData = bs.query_history_k_data_plus(
            stock.get_stock_code(),
            self._default_fields,
            start_date=stock.get_appear_time(),
            end_date=self._get_current_time,
            frequency=frequency,
            adjustflag=f"{adjustflag}"
        )
        if rs.error_code != '0':
            logger.error(
                f'query_history_k_data_plus respond error_code: {rs.error_code}, error_msg: {rs.error_msg}')
        yield from self._load_row_data(rs=rs)



bsq = BaoStockQuery()
