# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/05 16:59:48
@Author  :   kai.wang@westwell-lab.com 
'''
import csv
from typing import Generator,  List

from src.backtest.backtest_base import BackTestBase
from src.schema import StockTradeInfoSchema, TradeInfoSchema
from src.setting import logger


class BackTestKDJ(BackTestBase):
    def __init__(self) -> None:
        # 万二手续费, 百分比单位
        self.handling_fees_rate = 0.02
        self.backtest_type = "kdj"

    def backtest(self, stock_info: Generator):
        """
        提供相关算法
        3.1 K线是快速确认线——数值在90以上为超买,数值在10以下为超卖;

        3.2 D线是慢速主干线——数值在80以上为超买,数值在20以下为超卖;

        3.3 J线为方向敏感线,当J值大于90,特别是连续5天以上,股价至少会形成短期头部,反之J值小于10时,特别是连续数天以上,股价至少会形成短期底部。

        3.4 当K值由较小逐渐大于D值,在图形上显示K线从下方上穿D线,所以在图形上K线向上突破D线时,俗称金叉,即为买进的讯号。

        3.5 实战时当K,D线在20以下交叉向上,此时的短期买入的信号较为准确;如果K值在50以下,由下往上接连两次上穿D值,形成右底比左底高的「W底」形态时,后市股价可能会有相当的涨幅。

        3.6 当K值由较大逐渐小于D值,在图形上显示K线从上方下穿D线,显示趋势是向下的,所以在图形上K线向下突破D线时,俗称死叉,即为卖出的讯号。

        3.7 实战时当K,D线在80以上交叉向下,此时的短期卖出的信号较为准确;如果K值在50以上,由上往下接连两次下穿D值,形成右头比左头低的「M头」形态时,后市股价可能会有相当的跌幅。

        3.8 通过KDJ与股价背离的走势,判断股价顶底也是颇为实用的方法:

        ● 股价创新高,而KD值没有创新高,为顶背离,应卖出;

        ● 股价创新低,而KD值没有创新低,为底背离,应买入;

        ● 股价没有创新高,而KD值创新高,为顶背离,应卖出;

        ● 股价没有创新低,而KD值创新低,为底背离,应买入。

        3.9 需要注意的是KDJ顶底背离判定的方法,只能和前一波高低点时KD值相比,不能跳过去相比较。
        """
        pk, pd, pj = None, 0, 0
        all_trade_list = [
            []
        ]

        for g in self.index_calculate(stock_info):
            k, d, j, stock_schema = g
            if pk == None:
                pk, pd, pj = k, d, j
                continue
            # 底部金叉, 买入
            if k < 30 and d < 30 and \
                    pk < pd and k < d and all_trade_list[-1] is not []:
                all_trade_list[-1].append(stock_schema)
            # 持有一定时间后死叉, 卖出
            elif d > k and len(all_trade_list[-1]) > 5:
                all_trade_list[-1].append(stock_schema)
                all_trade_list.append([])
            elif all_trade_list[-1] is not []:
                all_trade_list[-1].append(stock_schema)

        trade_res_list = self.profit_summar(all_trade_list)
        return self.result_output(trade_res_list)

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

    def index_calculate(self, stock_info: Generator) -> Generator:
        """
        指标计算
        KDJ指标是计算n日内超买超卖情况。首先要计算周期(n日、n周等)的RSV值,即未成熟随机指标值,然后再计算K值、D值、J值等。一般n取9日。

        RSV(n日)=(Cn-Ln)/(Hn-Ln)*100

        Cn为第n日收盘价;Ln为n日内的最低价;Hn为n日内的最高价。

        其次,计算K值与D值:

        K值=2/3*前一日K值+1/3*当日RSV

        D值=2/3*前一日D值+1/3*当日K值

        J值=3*当日K值-2*当日D值
        """
        n = 9
        hign_list, low_list = [], []
        k, d, j = 50, 50, 0

        for stock_schema in stock_info:
            stock_schema: StockTradeInfoSchema
            if len(hign_list) < n:
                hign_list.append(stock_schema.high)
                low_list.append(stock_schema.low)
                continue
            hign = max(hign_list[-n:])
            low = min(low_list[-n:])
            close = stock_schema.close

            rsv = (close - low) / (hign - low) * 100 if hign != low else 0
            k = (2.0 / 3.0) * k + (1.0 / 3.0) * rsv
            d = (2.0 / 3.0) * d + (1.0 / 3.0) * k
            j = 3 * k - 2 * d
            yield k, d, j, stock_schema

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
