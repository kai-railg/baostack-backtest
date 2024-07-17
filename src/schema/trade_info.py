# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/10 10:44:06
@Author  :   kai.wang@westwell-lab.com 
'''

from pydantic import BaseModel, Field


class TradeInfoSchema(BaseModel):
    holding_time: int = Field(default=..., description="持有可交易天数")
    start_time: str = Field(default=..., description="开始持有时间")
    end_time: str = Field(default=..., description="结束时间")
    profit_rate: float = Field(default=..., description="收益率")
    profit_amount: float = Field(default=..., description="收益金额")
    handling_fees: float = Field(default=..., description="手续费")
    handling_fees_rate: float = Field(default=..., description="手续费率")
    backtest_type: str = Field(default=..., description="回测类型")
