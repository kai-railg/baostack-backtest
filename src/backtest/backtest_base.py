# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/05 10:50:26
@Author  :   kai.wang@westwell-lab.com 
'''
from abc import abstractmethod
from typing import Generator, List

from src.schema import StockTradeInfoSchema, TradeInfoSchema


class BackTestBase(object):
    def __init__(self) -> None:
        self.handling_fees_rate = 0
        self.backtest_type = ""

    @abstractmethod
    def backtest(self, stock_info: Generator):
        """
        外观函数
        """

    @abstractmethod
    def result_output(self, trade_res_list: List[TradeInfoSchema]):
        """
        输出结果
        """

    @abstractmethod
    def index_calculate(self, stock_info: Generator) -> Generator:
        """
        指标计算
        """

    @abstractmethod
    def profit_summar(self, trade_list: List[List[StockTradeInfoSchema]]) -> List[TradeInfoSchema]:
        """
        收益统计
        """
