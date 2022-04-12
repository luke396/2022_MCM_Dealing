import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from my_basic import Action
from my_basic import Action_
from my_macd import get_macd
from my_macd import get_macd_signal
from my_pairs import Pairs


def main():
    man = Action()  # 定义操作实体

    profits = []
    moneys = []
    date = pd.read_excel('Value_BitAndGoal.xlsx')
    bitcoin = date['Value'].rename('bitcoin')
    gold = date['USD (PM)'].rename('gold')

    gold_close = gold.values.reshape(-1)
    bitcoin_close = bitcoin.values.reshape(-1)
    gold_macd = get_macd(gold_close)['MACD']  # 提取macd数据集
    bitcoin_macd = get_macd(bitcoin_close)['MACD']
    date = np.where(~np.isnan(bitcoin_macd))[0]  # ~表示布尔值取反 剔除开始因macd算法产生的的nan
    macd_date = date[: 52]  # 日期上的前八十五天
    for date_yes in macd_date:
        date_now = date_yes + 1
        bit_signal = get_macd_signal(bitcoin_macd, date_now)
        gold_signal = get_macd_signal(gold_macd, date_now)

        if gold_signal != 0:
            # print('gold_signal,', gold_signal)
            name = 'gold'
            value = gold_close[date_now]

            if gold_signal == 1:
                # print('to look short')
                if man.is_short(name):  # 检测是否有空仓
                    # print('is short')
                    [money, profit] = man.short_close(name, value)
                    moneys.append(money)
                    profits.append(profit)
                man.long_open(name, value)

            elif gold_signal == -1:
                if man.is_long(name):  # 检测是否有多仓
                    # print('is long')
                    [money, profit] = man.long_close(name, value)
                    moneys.append(money)
                    profits.append(profit)
                man.short_open(name, value)
                # print('short number:', man.gold_short_num)
        if bit_signal != 0 and gold_signal == 0:
            # print('bit signal:', bit_signal)
            name = 'bitcoin'
            value = bitcoin_close[date_now]

            if bit_signal == 1:
                # print('to look short')
                if man.is_short(name):  # 检测是否有空仓
                    # print('is short')
                    [money, profit] = man.short_close(name, value)
                    moneys.append(money)
                    profits.append(profit)
                man.long_open(name, value)

            elif bit_signal == -1:
                if man.is_long(name):  # 检测是否有多仓
                    # print('is long')
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

    # print('--------------------------------------')
    # print('-----------Pairs Starting-------------')

    del_date_ends = []
    for i in range(19):
        num = int(85 + (i + 1) * 60)
        del_date_ends.append(num)
    del_date_ends.append(int(1265))
    del_date_ends = np.array(del_date_ends)
    obs_date_ends = del_date_ends - 60

    # obs_date_end = 85
    # del_date_end = 85 + 60

    for i in range(len(del_date_ends)):
        # print('Pairs %s' % (i + 1))
        obs_date_end = obs_date_ends[i]
        del_date_end = del_date_ends[i]
        pairs = Pairs(gold, bitcoin, obs_date_end, del_date_end)
        [money, profit] = pairs.open_and_close(man)
        moneys.append(money)
        profits.append(profit)

    return moneys


def model(money):
    man = Action_(money)  # 定义操作实体

    profits = []
    moneys = []
    date = pd.read_excel('Value_BitAndGoal.xlsx')
    bitcoin = date['Value'].rename('bitcoin')
    gold = date['USD (PM)'].rename('gold')

    gold_close = gold.values.reshape(-1)
    bitcoin_close = bitcoin.values.reshape(-1)
    gold_macd = get_macd(gold_close)['MACD']  # 提取macd数据集
    bitcoin_macd = get_macd(bitcoin_close)['MACD']
    date = np.where(~np.isnan(bitcoin_macd))[0]  # ~表示布尔值取反 剔除开始因macd算法产生的的nan
    macd_date = date[: 52]  # 日期上的前八十五天
    for date_yes in macd_date:
        date_now = date_yes + 1
        bit_signal = get_macd_signal(bitcoin_macd, date_now)
        gold_signal = get_macd_signal(gold_macd, date_now)

        if gold_signal != 0:
            # print('gold_signal,', gold_signal)
            name = 'gold'
            value = gold_close[date_now]

            if gold_signal == 1:
                # print('to look short')
                if man.is_short(name):  # 检测是否有空仓
                    # print('is short')
                    [money, profit] = man.short_close(name, value)
                    moneys.append(money)
                    profits.append(profit)
                man.long_open(name, value)

            elif gold_signal == -1:
                if man.is_long(name):  # 检测是否有多仓
                    # print('is long')
                    [money, profit] = man.long_close(name, value)
                    moneys.append(money)
                    profits.append(profit)
                man.short_open(name, value)
                # print('short number:', man.gold_short_num)
        if bit_signal != 0 and gold_signal == 0:
            # print('bit signal:', bit_signal)
            name = 'bitcoin'
            value = bitcoin_close[date_now]

            if bit_signal == 1:
                # print('to look short')
                if man.is_short(name):  # 检测是否有空仓
                    # print('is short')
                    [money, profit] = man.short_close(name, value)
                    moneys.append(money)
                    profits.append(profit)
                man.long_open(name, value)

            elif bit_signal == -1:
                if man.is_long(name):  # 检测是否有多仓
                    # print('is long')
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

    # print('--------------------------------------')
    # print('-----------Pairs Starting-------------')

    del_date_ends = []
    for i in range(19):
        num = int(85 + (i + 1) * 60)
        del_date_ends.append(num)
    del_date_ends.append(int(1265))
    del_date_ends = np.array(del_date_ends)
    obs_date_ends = del_date_ends - 60

    # obs_date_end = 85
    # del_date_end = 85 + 60

    for i in range(len(del_date_ends)):
        # print('Pairs %s' % (i + 1))
        obs_date_end = obs_date_ends[i]
        del_date_end = del_date_ends[i]
        pairs = Pairs(gold, bitcoin, obs_date_end, del_date_end)
        [money, profit] = pairs.open_and_close(man)
        moneys.append(money)
        profits.append(profit)

    return moneys[-1]


if __name__ == '__main__':
    moneys = main()


    # plt.style.use('_mpl-gallery')
    # fig, ax = plt.subplots()
    # ax.plot(moneys)
    # plt.figure(dpi=600)
    # ax.set(xlabel='Times', ylabel='Wallet',
    #        title='MACD with Pairs')
    # ax.grid()
    # fig.savefig("test.png", bbox_inches='tight')
    # plt.show()


