# -*- encoding: utf-8 -*-
'''
@Time    :   2024/07/03 14:04:23
@Author  :   kai.wang@westwell-lab.com 
'''

from src.service import (
    baostock_login,
    bsq,
    PullSHStock,
    PullSZStock
)
from src.backtest import BackTestKDJ

if __name__ == "__main__":
    ex_changes_list = [PullSHStock, PullSZStock]
    backtest_list = [BackTestKDJ]

    with baostock_login() as bsl:
        for stock_exchanges_cls in ex_changes_list:
            for stock in stock_exchanges_cls().get_stock_info():
                for bt_cls in backtest_list:
                    print("stock is ,", stock)
                    stock_info = bsq.query_k_data_plus(
                        stock=stock
                    )
                    print("stock schema is ", stock_info)
                    bt_result = bt_cls().backtest(stock_info)
                    print(bt_result[:100])
                    break
                break
            break
