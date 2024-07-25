# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/10 10:44:06
@Author  :   kai.wang@westwell-lab.com 
'''

from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo


class TradeInfoSchema(BaseModel):
    name: str = Field(default=..., description="股票名称")
    code: str = Field(default=..., description="股票代码")
    holding_time: int = Field(default=..., description="持有可交易天数")
    start_time: str = Field(default=..., description="开始持有时间")
    end_time: str = Field(default=..., description="结束持有时间")
    start_amount: float = Field(default=..., description="开始持有金额(元)")
    end_amount: float = Field(default=..., description="结束持有金额(元)")
    profit_rate: float = Field(default=..., description="收益率(%)")
    profit_amount: float = Field(default=..., description="收益金额(元)")
    handling_fees: float = Field(default=..., description="手续费(元)")
    handling_fees_rate: float = Field(default=..., description="手续费率(%)")
    backtest_type: str = Field(default=..., description="回测类型")

    def get_csv_fields(self) -> list:
        fields = []
        for field_name, field_info in self.model_fields.items():
            field_info: FieldInfo
            fields.append(field_info.description)
        return fields

    def get_csv_row(self) -> list:
        row = []
        for field_name, field_info in self.model_fields.items():
            row.append(getattr(self, field_name))
        return row
