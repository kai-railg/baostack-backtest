# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/05 10:50:26
@Author  :   kai.wang@westwell-lab.com 
'''
import csv
from abc import abstractmethod
from typing import Generator, List

from src.schema import StockTradeInfoSchema, TradeInfoSchema
from src.setting import logger


class BackTestBase(object):
    def __init__(self) -> None:
        self.handling_fees_rate = 0
        self.backtest_type = ""

    @abstractmethod
    def backtest(self, stock_info: Generator):
        """
        外观函数
        """

    def result_output(self, trade_res_list: List[TradeInfoSchema]):
        """
        输出结果
        """
        if not trade_res_list:
            logger.info("No trade result")
            return
        all_holding_time = 0
        total_profit_rate = 0
        total_profit_amount = 0

        result = []
        msg = f"Trade detail, stock is {trade_res_list[0].name, trade_res_list[0].code}"
        for trade_schema in trade_res_list:
            profit_rate = trade_schema.profit_rate * \
                (1-trade_schema.handling_fees_rate)
            result.append(
                {
                    "profit_rate": f"{round(profit_rate, 3)}%",
                    "holding_time": trade_schema.holding_time,
                    "start_time":  trade_schema.start_time,
                    "end_time": trade_schema.end_time,
                    "profit_amount":  trade_schema.profit_amount,
                    "backtest_type": trade_schema.backtest_type,
                }
            )

            all_holding_time += trade_schema.holding_time
            total_profit_rate += profit_rate
            total_profit_amount += trade_schema.profit_amount

        csv_fieldnames = [
            "profit_rate",
            "holding_time",
            "start_time",
            "end_time",
            "profit_amount",
            "backtest_type"
        ]
        csv_f = open(
            f"./src/output/{trade_res_list[0].name}-{trade_res_list[0].code}-{self.backtest_type}-backtest.csv", 'w', newline='')
        writer = csv.DictWriter(csv_f, fieldnames=csv_fieldnames)
        writer.writeheader()

        for num, res in enumerate(result, start=1):
            msg += f"\nTrade number is {num}, \n"
            msg += f"    profit_rate: {res['profit_rate']}%, \n"
            msg += f"    holding_time: {res['holding_time']}, \n"
            msg += f"    start_time: {res['start_time']}, \n"
            msg += f"    end_time: {res['end_time']}, \n"
            msg += f"    profit_amount: {res['profit_amount']}, \n"
            msg += f"    backtest_type: {res['backtest_type']}, \n"
            writer.writerow(res)
        csv_f.close()

        msg += f"Total holding time is {all_holding_time}, \n"
        msg += f"Total profit rate is {total_profit_rate}%, \n"
        msg += f"Total profit amount is {total_profit_amount}"
        logger.info(msg)
        return msg

    @abstractmethod
    def index_calculate(self, stock_info: Generator) -> Generator:
        """
        指标计算
        """

    def profit_summar(self, trade_list: List[List[StockTradeInfoSchema]]) -> List[TradeInfoSchema]:
        """
        收益统计
        """
        trade_result = []
        for stock_info_list in trade_list:
            if not stock_info_list:
                continue

            pct = round(sum([stock.pctChg for stock in stock_info_list]), 2)
            trade_result.append(TradeInfoSchema(
                holding_time=len(stock_info_list),
                start_time=stock_info_list[0].date,
                end_time=stock_info_list[-1].date,
                profit_rate=pct,
                profit_amount=0,
                handling_fees=0,
                handling_fees_rate=self.handling_fees_rate,
                backtest_type=self.backtest_type,
                name=stock_info_list[0].name,
                code=stock_info_list[0].code,
            ))
        return trade_result
