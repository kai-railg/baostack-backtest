# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/03 14:23:35
@Author  :   kai.wang@westwell-lab.com 
'''

from enum import Enum
from pydantic import BaseModel, Field

class exchanges_enum(Enum):
    sh = 'sh'
    sz = 'sz'

class StockInfoSchema(BaseModel):
    code: str = Field(default=..., description="股票代码")
    name: str = Field(default=..., description="股票名称")
    exchanges_alias: exchanges_enum = Field(..., description="交易所别名")

    industry: str = Field(default="", description="行业")
    industry_code: str = Field(default="", description="行业代码")

    def get_stock_code(self) -> str:
        return self.exchanges_alias.value + "." + str(self.code)
