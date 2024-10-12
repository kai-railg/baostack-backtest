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
from src.select_stock import (
    SelectStockAmountLowUpline
)
from src.backtest import (
    BackTestKDJ,
    BackTestTopRebound,
    BackTestAmountSurge
)

if __name__ == "__main__":
    ex_changes_list = [PullSHStock, PullSZStock]
    backtest_list = [BackTestAmountSurge]

    with baostock_login() as bsl:
        for stock_exchanges_cls in ex_changes_list:
            scores = []
            for stock in stock_exchanges_cls().get_stock_info():
                stock_info = bsq.query_k_data_plus(
                        stock=stock,
                        start_date="2024-09-24"
                )
                score = SelectStockAmountLowUpline().select(stock_info)
                scores.append([score, stock.name])
            scores.sort(key=lambda x: x[0], reverse=True)
            for score, name in scores[:20]:
                print(f"{name} {score}")
                    

            #     for bt_cls in backtest_list:
            #         print("stock is ,", stock)
            #         stock_info = bsq.query_k_data_plus(
            #             stock=stock
            #         )
            #         print("stock schema is ", stock_info)
            #         bt_result = bt_cls().backtest(stock_info)
            #         print(bt_result[:350], "\n...\n", bt_result[-400:])
            #         break
            #     break
            # break
