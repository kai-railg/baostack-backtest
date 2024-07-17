# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/03 14:04:23
@Author  :   kai.wang@westwell-lab.com 
'''

from src.schema import StockInfoSchema
from src.service import (
    baostock_login,
    bsq,
    PullSHStock,
    PullSZStock
)

if __name__ == "__main__":
    with baostock_login() as bsl:
        for stock_exchanges_cls in [PullSHStock, PullSZStock]:
            for stock in stock_exchanges_cls().get_stock_info():
                print("stock is ,", stock)
                for stock_schema in bsq.query_k_data_plus(
                    stock=stock
                ):
                    print("stock schema is ",stock_schema)
                    break
                break
