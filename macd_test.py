import numpy as np
import pandas as pd

from my_basic import Action
from my_macd import get_macd
from my_macd import get_macd_signal

bitcoin = pd.read_excel('BitCleand.xlsx', index_col=0)
gold = pd.read_excel('GoalCleand.xlsx', index_col=0)

gold_close = gold.values.reshape(-1)
bitcoin_close = bitcoin.values.reshape(-1)

gold_macd = get_macd(gold_close)['MACD']  # 提取macd数据集
bitcoin_macd = get_macd(bitcoin_close)['MACD']

date = np.where(~np.isnan(bitcoin_macd))[0]  # ~表示布尔值取反
macd = bitcoin_macd
close = bitcoin_close
man = Action()

for date_yes in date[:-1]:
    name = 'bitcoin'
    date_now = date_yes + 1
    value = close[date_now]
    # number = (man.get_money()) // value
    signal = get_macd_signal(macd, date_now)
    print(signal)
    if signal == -1:  # 信号取反
        # print('to look short')
        if man.is_short(name):  # 检测是否有空仓
            print('is short')
            man.short_close(name, value)
        man.long_open(name, value)

    elif signal == 1:
        if man.is_long(name):  # 检测是否有多仓
            print('is long')
            man.long_close(name, value)
        man.short_open(name, value)
        # print('short number:', man.gold_short_num)
