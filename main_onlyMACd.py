import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from my_basic import Action
from my_macd import get_macd
from my_macd import get_macd_signal

man = Action()  # 定义操作实体

date = pd.read_excel('Value_BitAndGoal.xlsx')
bitcoin = date['Value'].rename('bitcoin')
gold = date['USD (PM)'].rename('gold')

gold_close = gold.values.reshape(-1)
bitcoin_close = bitcoin.values.reshape(-1)
gold_macd = get_macd(gold_close)['MACD']  # 提取macd数据集
bitcoin_macd = get_macd(bitcoin_close)['MACD']

date = np.where(~np.isnan(bitcoin_macd))[0]  # ~表示布尔值取反 剔除开始因macd算法产生的的nan

profits = []
moneys = []

macd_date = date[: -1]
for date_yes in macd_date:
    date_now = date_yes + 1
    bit_signal = get_macd_signal(bitcoin_macd, date_now)
    gold_signal = get_macd_signal(gold_macd, date_now)

    if gold_signal != 0:
        print('gold_signal,', gold_signal)
        name = 'gold'
        value = gold_close[date_now]

        if gold_signal == 1:
            # print('to look short')
            if man.is_short(name):  # 检测是否有空仓
                print('is short')
                [money, profit] = man.short_close(name, value)
                moneys.append(money)
                profits.append(profit)
            man.long_open(name, value)

        elif gold_signal == -1:
            if man.is_long(name):  # 检测是否有多仓
                print('is long')
                [money, profit] = man.long_close(name, value)
                moneys.append(money)
                profits.append(profit)
            man.short_open(name, value)
            # print('short number:', man.gold_short_num)

    if bit_signal != 0 and gold_signal == 0:
        print('bit signal:', bit_signal)
        name = 'bitcoin'
        value = bitcoin_close[date_now]

        if bit_signal == 1:
            # print('to look short')
            if man.is_short(name):  # 检测是否有空仓
                print('is short')
                [money, profit] = man.short_close(name, value)
                moneys.append(money)
                profits.append(profit)
            man.long_open(name, value)

        elif bit_signal == -1:
            if man.is_long(name):  # 检测是否有多仓
                print('is long')
                [money, profit] = man.long_close(name, value)
                moneys.append(money)
                profits.append(profit)
            man.short_open(name, value)
            # print('short number:', man.gold_short_num)

    if date_yes == macd_date[-1]:  # 强制平仓
        if man.is_long('gold'):
            [money, profit] = man.long_close('gold', gold_close[date_now])
            moneys.append(money)
            profits.append(profit)
        elif man.is_long('bitcoin'):
            [money, profit] = man.long_close('bitcoin', bitcoin_close[date_now])
            moneys.append(money)
            profits.append(profit)
        elif man.is_short('gold'):
            [money, profit] = man.short_close('gold', gold_close[date_now])
            moneys.append(money)
            profits.append(profit)
        elif man.is_short('bitcoin'):
            [money, profit] = man.short_close('bitcoin', bitcoin_close[date_now])
            moneys.append(money)
            profits.append(profit)

plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()
ax.plot(bitcoin_macd)
plt.figure(dpi=600)
ax.set(xlabel='Times', ylabel='Bitcoin_MACD',
       title='MACD')
ax.grid()
fig.savefig("test.png", bbox_inches='tight')
plt.show()
