from datetime import datetime
from datetime import timedelta

import numpy as np
import pandas as pd

'''剔除比特币加各种，黄金交易的休息日'''
bit = pd.read_excel('BCHAIN-MKPRU_DateChanged.xlsx', index_col=0)
gold = pd.read_excel('LBMA-GOLD_DateChanged.xlsx', index_col=0)

# 对gold的缺失值进行处理
# 由于价格具有不确定性，故缺失值采取 (before+tomorrow)/random(0,1){0-1}开区间符合正态分布的随机数
nothing = gold[gold.isnull().values]

for i in nothing.index.to_list():
    index = datetime.date(datetime.strptime(i, '%Y-%m-%d'))
    tomorrow = str(index + timedelta(days=1))
    yesterday = str(index + timedelta(days=-1))
    if yesterday in gold.index and tomorrow in gold.index:
        value_yes = gold.loc[yesterday, :]
        value_tom = gold.loc[tomorrow, :]
        value_now = (value_tom + value_yes) * np.random.uniform(0.495, 0.505, 1)
    elif yesterday not in gold.index and tomorrow in gold.index:
        value_tom = gold.loc[tomorrow, :]
        value_now = 2 * value_tom * np.random.uniform(0.495, 0.505, 1)
    elif yesterday in gold.index and tomorrow not in gold.index:
        value_yes = gold.loc[yesterday, :]
        value_now = 2 * value_yes * np.random.uniform(0.495, 0.505, 1)
    else:  # 无临值时
        value_now = gold.dropna(axis=0, how='any').values.mean()  # 去空值的均值

    gold.loc[str(index), :] = value_now

index = gold.index.to_list()
bit_ = bit.loc[index]  # 日期匹配

data = pd.concat([bit_, gold], axis=1)
# data = data.dropna(axis=0, how='any')
# bit__ = bit_.dropna(axis=0, how='any')
# gold_ = gold.dropna(axis=0, how='any')

data.to_excel('Value_BitAndGoal.xlsx')
# bit.isnull().values.any()
bit.to_excel('BitCleand.xlsx')  # bit没有缺失值
gold.to_excel('GoalCleand.xlsx')
