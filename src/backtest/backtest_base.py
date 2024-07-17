# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/05 10:50:26
@Author  :   kai.wang@westwell-lab.com 
'''
import enum
from typing import Generator, List

from src.schema import StockTradeInfoSchema, TradeInfoSchema


class BackTestBase(object):
    def __init__(self) -> None:
        # 万二手续费
        self.handling_fees_rate = 0.02 * 0.01
        self.backtest_type = ""

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
            if k < 20 and d < 20 and \
                    pk < pd and k < d:
                all_trade_list[-1].append(stock_schema)
            # 持有一定时间后死叉, 卖出
            elif d > k and len(all_trade_list[-1]) > 5:
                all_trade_list[-1].append(stock_schema)
                all_trade_list.append([])

        trade_res_list = self.profit_summar(all_trade_list)
        self.result_output(trade_res_list)

    def result_output(self, trade_res_list: List[TradeInfoSchema]):
        """
        输出结果
        """
        all_holding_time = 0
        total_profit_rate = 0
        total_profit_amount = 0
        for trade_schema in trade_res_list:
            pass

#     holding_time: int = Field(default=..., description="持有可交易天数")
    # start_time: str = Field(default=..., description="开始持有时间")
    # end_time: str = Field(default=..., description="结束时间")
    # profit_rate: float = Field(default=..., description="收益率")
    # profit_amount: float = Field(default=..., description="收益金额")
    # handling_fees: float = Field(default=..., description="手续费")
    # handling_fees_rate: float = Field(default=..., description="手续费率")
    # backtest_type: str = Field(default=..., description="回测类型")


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
            hign = max(hign_list[:-n])
            low = min(low_list[:-n])
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

            pct = sum([stock.pctChg for stock in stock_info_list])
            trade_result.append(TradeInfoSchema(
                holding_time=len(stock_info_list),
                start_time=stock_info_list[0].date,
                end_time=stock_info_list[-1].date,
                profit_rate=round(pct / 100, 2),
                profit_amount=0,
                handling_fees=0,
                handling_fees_rate=self.handling_fees_rate,
                backtest_type=self.backtest_type
            ))
        return trade_result
