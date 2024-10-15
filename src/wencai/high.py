# -*- encoding: utf-8 -*-
"""
@Time     :   2024/10/12 14:01:31
@Version  :   python3.11
"""
import collections

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

mp_type = collections.defaultdict(list)
mp_days = collections.defaultdict(list)
for index, row in res.iterrows():
    
    data = row.to_dict()
    name = data["股票简称"]
    data.pop("涨停明细数据[20241015]", None)
    for t in data.get('涨停原因类别[20241015]', "其他").split("+"):
        mp_type[t].append(name)
    mp_days[data.get('连续涨停天数[20241015]')].append(name)
    print(data)
    input()

for k, v in mp_type.items():
    print(f"概念: {k} ", v)
for k, v in mp_days.items():
    print(f"连板: {k} ", v)