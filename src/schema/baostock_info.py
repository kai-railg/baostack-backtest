# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/03 15:48:59
@Author  :   kai.wang@westwell-lab.com 
'''
from pydantic import BaseModel, Field, model_validator, field_validator

class BaoStockInfoSchema(BaseModel):
    # {'date': '2024-07-02',
    # 'code': 'sh.600649',
    # 'open': '3.5300000000',
    # 'high': '3.7800000000',
    # 'low': '3.4800000000',
    # 'close': '3.6200000000',
    # 'preclose': '3.5300000000',
    #  'volume': '79313281',
    # 'amount': '289803306.3200',
    # 'adjustflag': '2',
    # 'turn': '3.135400',
    # 'tradestatus': '1',
    # 'pctChg': '2.549600',
    # 'isST': '0'}
    date: str= Field(..., alias='date', description="交易所行情日期	")
    code: str= Field(..., alias='code', description="证券代码")
    open: float = Field(..., alias='open', description="开盘价")
    high: float = Field(..., alias='high', description="最高价")
    low: float = Field(..., alias='low', description="最低价")
    close: float = Field(..., alias='close', description="收盘价")
    preclose: float = Field(..., alias='preclose', description="前收盘价")
    volume: int = Field(..., alias='volume', description="成交量（累计 单位:股）")
    amount: float = Field(..., alias='amount', description="成交额（单位:人民币元）")
    adjustflag: int = Field(..., alias='adjustflag', description="复权状态(1:后复权, 2:前复权,3:不复权）")	
    turn: float = Field(..., alias='turn', description="换手率	[指定交易日的成交量(股)/指定交易日的股票的流通股总股数(股)]*100%")
    tradestatus: int = Field(..., alias='tradestatus', description="交易状态(1:正常交易 0:停牌）")
    pctChg: float = Field(..., alias='pctChg', description="涨跌幅（百分比）	日涨跌幅=[(指定交易日的收盘价-指定交易日前收盘价)/指定交易日前收盘价]*100%")
    isST: int = Field(..., alias='isST', description="是否ST股,1是,0否")

    @model_validator(mode="after")
    def after(self):
        self.pctChg /= 100

    
    @field_validator('turn', mode="before")
    def parse_value(cls, v):
        if isinstance(v, str):
            if v == "":
                return 0.0
            try:
                return float(v)
            except ValueError:
                raise ValueError("Invalid float value")
        return v