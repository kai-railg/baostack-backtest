# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/03 14:23:35
@Author  :   kai.wang@westwell-lab.com 
'''

from enum import Enum
from pydantic import BaseModel, Field, constr


class ExchangesEnum(Enum):
    sh = 'sh'
    sz = 'sz'


class StockInfoSchema(BaseModel):
    code: str = Field(default=..., description="股票代码")
    name: str = Field(default=..., description="股票名称")
    exchanges_alias: ExchangesEnum = Field(..., description="交易所别名")

    industry: str = Field(default="", description="行业")
    industry_code: str = Field(default="", description="行业代码")

    appear_time: constr(pattern=r'^\d{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$') # type: ignore
    market: str =  Field(default="A", description="板块")
    company_name: str =  Field(default="", description="公司名称")
    english_name: str =  Field(default="", description="英文名称")
    register_address: str =  Field(default="", description="注册地址")
    total_capital: str =  Field(default="", description="总股本")
    circulation_capital: str =  Field(default="", description="流通股本")
    website: str =  Field(default="", description="公司网址")
    no_profit: str =  Field(default="", description="未盈利")
    vote_differ_arrange: str =  Field(default="", description="具有表决权差异安排")
    protocol_control_architecture: str =  Field(default="", description="具有协议控制架构")

    def get_stock_code(self) -> str:
        return self.exchanges_alias.value + "." + str(self.code)

    def get_appear_time(self) -> str:
        return self.appear_time[:4] + "-" + self.appear_time[4:6] + "-" + self.appear_time[6:]
