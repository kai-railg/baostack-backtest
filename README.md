1. 拉取上交所，深交所的股票列表数据, 保存并反序列化
2. 从 baostaock 获取指定的股票交易数据, 保存并反序列化
3. 对股票交易数据进行回测，支持的回测类型有:
    1. kdj
    2. boll
    3. macd
    4. 波段
    5. 行情
    6. 均线

- Start
    
    ```python
    # pip install -r requirements.txt 
    python main.py
    ```