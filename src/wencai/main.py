# -*- encoding: utf-8 -*-
"""
@Time     :   2024/10/12 14:01:31
@Version  :   python3.11
"""
from pandas import DataFrame
import pywencai

# res: DataFrame = pywencai.get(
#     query='不包含st; 只包含60、30和00开头的股票',
#     sort_key='换手率',
#     sort_order='asc',
#     loop=True,
#     query_type="stock",
# )

res: DataFrame = pywencai.get(
    query='不包含st; 不包含科创板; 今日涨停',
    sort_key='换手率',
    sort_order='asc',
    loop=True,
    query_type="stock",
)

# res: DataFrame = pywencai.get(
#     query='不包含st; 只包含60、30和00开头的股票; 成交量环比增长率大于100%; 今日阳线未涨停',
#     sort_key='换手率',
#     sort_order='asc',
#     loop=True,
#     query_type="stock",
# )

# res: DataFrame = pywencai.get(
#     query='不包含st; 只包含60、30和00开头的股票; 量能持续缩减3天以上; 今日有长影线或长下影线;今日小阳线; 近30天内有过涨停',
#     sort_key='换手率',
#     sort_order='asc',
#     loop=True,
#     query_type="stock",
# )

for index, row in res.iterrows():
    data = row.to_dict()
    data.pop("涨停明细数据[20241015]", None)
    print(data)
    input()


# res: DataFrame = pywencai.get(
#     query='神马电力',
#     sort_key='换手率',
#     sort_order='asc',
#     query_type="stock",
# )


# print(res.keys())
# for index, row in res["所属概念列表"].iterrows():
#     print(row.to_dict()["诊股概念分类名称"])
#     # input()
