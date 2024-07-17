# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/05 16:59:48
@Author  :   kai.wang@westwell-lab.com 
'''


# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/05 10:50:26
@Author  :   kai.wang@westwell-lab.com 
'''
from typing import Generator

from src.backtest.backtest_base import BackTestBase
from src.schema import StockInfoSchema


class BackTestKDJ(BackTestBase):
    def __init__(self) -> None:
        super().__init__()

    def backtest(self, stock_schema: StockInfoSchema):
        """
        提供相关算法
        """
        for index in self.index_calculate(stock_schema):
            pass

    def result_output(self):
        """
        输出结果
        """
        pass

    def index_calculate(self, stock_schema: StockInfoSchema):
        """
        指标计算
        """
        while True:
            yield

    def profit_summar():
        """
        收益统计
        """
        pass