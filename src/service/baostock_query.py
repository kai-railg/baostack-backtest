# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/03 14:19:21
@Author  :   kai.wang@westwell-lab.com 
'''
from typing import List
from datetime import datetime


import baostock as bs
import pandas as pd
from baostock.data.resultset import ResultData

from src.setting import logger
from src.schema import StockInfoSchema, BaoStockInfoSchema

__all__ = ["bsq"]


class BaoStockQuery(object):
    def __init__(self) -> None:
        pass

    @property
    def _default_fields(self):
        return "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"

    def _get_row_data(self, rs: ResultData) -> List[BaoStockInfoSchema]:
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        # result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
        result_filter = result[result["isST"] == "0"]
        result_filter = result[result["tradestatus"] == "1"]
        result = []
        for row in result_filter.iloc:
            row_dict = row.to_dict()
            result.append(BaoStockInfoSchema(**{
                k: row_dict[k] for k in self._default_fields.split(",") if k in row_dict
            }))
        return result

    @property
    def _get_current_year(self) -> str:
        return datetime.now().year

    def query_k_data_plus(self, stock: StockInfoSchema, adjustflag=2) -> pd.DataFrame:
        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs: ResultData = bs.query_history_k_data_plus(
            stock.get_stock_code(),
            self._default_fields,
            start_date=f'{self._get_current_year-15}-01-01',
            end_date=f'{self._get_current_year+1}-01-01',
            frequency="d",
            adjustflag=f"{adjustflag}"
        )
        if rs.error_code != '0':
            logger.error(
                f'query_history_k_data_plus respond error_code: {rs.error_code}, error_msg: {rs.error_msg}')
        return self._get_row_data(rs=rs)

    def query_k_data_plus_many(self, stock_list: list[StockInfoSchema]):
        pass


bsq = BaoStockQuery()
