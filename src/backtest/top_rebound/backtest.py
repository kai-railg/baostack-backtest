# -*- encoding: utf-8 -*-
"""
@Time     :   2024/09/19 13:45:20
@Version  :   python3.11
"""


from typing import Generator,  List

from src.backtest.backtest_base import BackTestBase
from src.schema import StockTradeInfoSchema, TradeInfoSchema
from src.setting import logger


class BackTestTopRebound(BackTestBase):
    def __init__(self) -> None:
        super().__init__()
        self.backtest_type = "龙头反弹"

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
        high_idx = None
        for i, stock in enumerate(stock_info):
            if i < 4:
                continue
            if i == len(stock_info) -1:
                continue

            stock: StockTradeInfoSchema
            if high_idx is None:
                if stock.high == stock.close:
                    high_idx = i
                continue
            if i - high_idx > 30:
                high_idx = None
                continue

            score = 0
            pre_stock = stock_info[i - 1]
            # 成交量
            score += stock.amount / pre_stock.amount
            score += sum([stock_info[i-j-1].amount / stock_info[i-j].amount  for j in range(1, 4)])
            # # 跌幅
            # score += 1 - stock.close / stock_info[high_idx].close

            # 上影线
            score += stock.high / stock.close
            # 下影线
            score += stock.close / stock.low
            
            result.append([score, i])
        result.sort(reverse=True, key=lambda x: x[0])
        for score, idx in result[:10]:
            stock=stock_info[idx]
            print(score, stock.name, stock.date)
        return [[stock_info[idx], stock_info[idx+1]] for score, idx in result]

