# -*- encoding: utf-8 -*-
"""
@Time     :   2024/09/19 16:58:45
@Version  :   python3.11
"""




from typing import Generator,  List

from src.backtest.backtest_base import BackTestBase
from src.schema import StockTradeInfoSchema, TradeInfoSchema
from src.setting import logger


class BackTestAmountSurge(BackTestBase):
    def __init__(self) -> None:
        super().__init__()
        self.backtest_type = "量能激增"

    def backtest(self, stock_info: Generator):
        """
        1. 近期N天内有过涨停或者炸版
        2. 股价处于下跌状态
        3. 非首日的缩量微跌， 开盘价接近收盘价，有长上影线或下影线
        4. 权重计算,
            1.有涨跌停+10, 炸版+5, score = (day2 - day1 + 1) // 10 * -1
            2.下跌缩量状态, score = sum(day2...day0)
        """
        all_trade_list = []

        for stocks in self.index_calculate(stock_info):
            all_trade_list.append(stocks)

        trade_res_list = self.profit_summar(all_trade_list)
        return self.result_output(trade_res_list)

    def index_calculate(self, stock_info: Generator) -> Generator:
        """

        """
        stock_info = [stock for stock in list(stock_info) if stock.amount]
        result = [ ]

        for i, stock in enumerate(stock_info):
            if i == len(stock_info) -1:
                continue
            pre_stock = stock_info[i - 1]
            score = 0
            score += min(stock.amount / pre_stock.amount, 2)
            score += (stock.high / stock.close) * 5
            if score < 1.05:
                continue
            result.append([score, i])
        result.sort(reverse=True, key=lambda x: x[0])
        for score, idx in result[:20]:
            stock=stock_info[idx]
            print(score, stock.name, stock.date)
        return [[stock_info[idx], stock_info[idx+1]] for score, idx in result]

