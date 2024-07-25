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
        self.handling_fees_rate = 0.02
        self.backtest_type = ""
        self.base_money = 10000

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

        csv_fieldnames: List[str] = trade_res_list[0].get_csv_fields()
        max_length = max([len(i) for i in csv_fieldnames]) + 1

        with open(file=f"./src/output/{trade_res_list[0].name}-{trade_res_list[0].code}-{self.backtest_type}-backtest.csv",
                  mode='w',
                  newline='') as csv_f:

            writer = csv.writer(csv_f)
            writer.writerow(csv_fieldnames)

            all_holding_time = 0
            total_profit_rate = 0
            total_profit_amount = 0
            handling_fees = 0

            msg = f"Trade detail, stock is {trade_res_list[0].name, trade_res_list[0].code}"

            for num, trade_schema in enumerate(trade_res_list, start=1):
                msg += f"\n交易次数: {num}, \n"

                row = trade_schema.get_csv_row()
                for dec, col in zip(csv_fieldnames, row):
                    msg += f"    {dec.ljust(max_length)}: {col}\n"

                all_holding_time += trade_schema.holding_time
                total_profit_rate += trade_schema.profit_rate
                total_profit_amount += trade_schema.profit_amount
                handling_fees += trade_schema.handling_fees

                writer.writerow(row)

        msg += f"Total holding days are {all_holding_time}, \n"
        msg += f"Total profit rate is {self.round(total_profit_rate)}%, \n"
        msg += f"Total profit amount is {self.round(total_profit_amount)}\n"
        msg += f"Total handling fees is {self.round(handling_fees)}\n"
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

        start_money = self.base_money
        for stock_info_list in trade_list:
            if not stock_info_list:
                continue

            pct = self.round(
                sum([stock.pctChg for stock in stock_info_list]), 2)

            end_money = self.round(start_money * (1 + pct / 100))
            handling_fees = round(end_money * self.handling_fees_rate * 0.01)
            end_money -= handling_fees
            profit_amount = self.round(end_money - start_money)

            trade_result.append(TradeInfoSchema(
                holding_time=len(stock_info_list),
                start_time=stock_info_list[0].date,
                end_time=stock_info_list[-1].date,
                start_amount=start_money,
                end_amount=end_money,
                profit_rate=round(pct - self.handling_fees_rate),
                profit_amount=profit_amount,
                handling_fees=handling_fees,
                handling_fees_rate=self.handling_fees_rate,
                backtest_type=self.backtest_type,
                name=stock_info_list[0].name,
                code=stock_info_list[0].code,
            ))

            start_money = end_money
        return trade_result

    @classmethod
    def round(cls, number, nd=2):
        return round(float(number), nd)
