# -*- encoding: utf-8 -*-
"""
@Time     :   2024/09/19 16:58:45
@Version  :   python3.11
"""




from typing import Generator,  List

from schema.stock_info import StockInfoSchema
from service.stock_info import StockInfo
from src.backtest.backtest_base import BackTestBase
from src.schema import StockTradeInfoSchema, TradeInfoSchema
from src.setting import logger


class BackTestAmountLowUpline(BackTestBase):
    def __init__(self) -> None:
        super().__init__()
        self.backtest_type = "连续下跌缩量并小阳线"

    def backtest(self, stock_info: Generator):

        all_trade_list = []

        return self.index_calculate(stock_info)

        trade_res_list = self.profit_summar(all_trade_list)
        return self.result_output(trade_res_list)

    def index_calculate(self, stock_info: Generator) -> Generator:
        """

        """
        stock_info = [stock for stock in list(stock_info) if stock.amount]
        stock_info = stock_info[-4:]

        score = 1
        for i, stock in enumerate(stock_info):
            if i == 0:
                continue
            pre_stock = stock_info[i - 1]
            score *= round(pre_stock.amount / stock.amount, 2)
            if i == len(stock_info) -1:
                score *= 1.15 if round.pct > 1 else 0.85
            


        return score, stock_info

