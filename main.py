# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/03 14:04:23
@Author  :   kai.wang@westwell-lab.com 
'''

from src.schema import  StockInfoSchema
from src.service import baostock_login, bsq

if __name__ == "__main__":
    with baostock_login() as rs:
        result = bsq.query_k_data_plus(
            StockInfoSchema(
                code="600649",
                name="城投控股",
                exchanges_alias="sh",
            )
        )
        print(result[0])

