import numpy as np
import pandas as pd
from statsmodels.api import OLS
from statsmodels.api import add_constant
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint

from my_basic import Action


class Pairs:
    def __init__(self, gold, bitcoin, obs_date_end, del_date_end):
        self.bitcoin = bitcoin
        self.gold = gold

        obs_per = 85  # 观察期 # 85这里可以出一个协整的数据
        del_per = 60  # 交易期

        # 改变他俩
        self.obs_date_end = obs_date_end
        self.del_date_end = del_date_end

        self.gold_obs = self.gold[:self.obs_date_end]
        self.gold_deal = self.gold[self.obs_date_end:self.del_date_end]
        self.bit_obs = self.bitcoin[:self.obs_date_end]
        self.bit_deal = self.bitcoin[self.obs_date_end:self.del_date_end]

    def ADF_and_coi(self):
        # 首先通过ADF检验，判断两个序列是否为一阶单整
        gold_obs = np.reshape(self.gold_obs, -1)
        bit_obs = np.reshape(self.bit_obs, -1)
        gold_obs_diff = np.diff(gold_obs)
        bit_obs_diff = np.diff(bit_obs)
        gold_obs_adf = adfuller(gold_obs_diff)
        print('gold_diff adf:', gold_obs_adf[0] < gold_obs_adf[4]['1%'])
        bit_obs_adf = adfuller(bit_obs_diff)  # 均一阶单整
        print('bitcoin_diff adf:', bit_obs_adf[0] < bit_obs_adf[4]['1%'])

        [t, p, arr] = coint(bit_obs, gold_obs)  # 判断是否协整， 通过t值与1%
        print('obs=85, Cointegration:', t < arr[0])

        X = add_constant(bit_obs)  # 不添加常数列则结果无常数
        y = gold_obs
        ols_result = OLS(y, X).fit()  # 55 -- bit--0.5649
        print(ols_result.summary())  # OLS方程获取beta
        bate = ols_result.params[1]

        return bate

    def get_pst(self):
        """获取交易期的pst"""
        ps = np.log10(self.gold) - np.log10(self.bitcoin)  # 股票价差
        ps_obs = ps[:self.obs_date_end]
        ps_deal = ps[self.obs_date_end:self.del_date_end]
        ps_obs_mean = np.mean(ps_obs)  # 观察期价差均值
        ps_obs_std = np.sqrt((1 / (85 - 1)) * ((ps_obs - ps_obs_mean) ** 2).sum())  # 观察期价差标准差
        pst = (ps_deal - ps_obs_mean) / ps_obs_std  # 交易价差
        return pst

    def get_open_date(self):
        pst = self.get_pst()
        # print('pst:', pst)
        ope_date = None
        if pst.loc[(2 < abs(pst.values)) & (abs(pst.values < 3))].size != 0:
            GGR_signal = pst.loc[(2 < abs(pst.values)) & (abs(pst.values < 3))].index[0]  # GGR
            # print('GGR!')
            # 获取建仓日期
            waiting = pst.loc[GGR_signal + 1:]
            # print('open!')
            ope = False
            ope_date = 0
            for i in waiting.index[:-1]:
                if pst.loc[i + 1] < pst.loc[i]:
                    ope = True
                    ope_date = i + 1
                if ope:
                    break
        return ope_date

    def open_and_close(self, man):
        # 对交易期价格数值进行调整
        money = man.money
        profit = 0
        ope_date = self.get_open_date()
        if ope_date is not None:
            pst = self.get_pst()

            gold_pc = (self.gold_deal - np.mean(self.gold_obs)) / (np.std(self.gold_obs))  # price changed
            bit_pc = (self.bit_deal - np.mean(self.bit_obs)) / (np.std(self.bit_obs))

            # 开仓
            gold_long = False
            bit_long = False
            if gold_pc.loc[ope_date] > bit_pc.loc[ope_date]:
                # if man.is_short('bitcoin'):
                #     man.short_close('bitcoin', self.bitcoin.loc[ope_date])
                # elif man.is_short('gold'):
                #     man.short_close('gold', self.gold.loc[ope_date])
                # elif man.is_long('gold'):
                #     man.long_close('gold', self.gold.loc[ope_date])
                man.long_open('bitcoin', self.bitcoin.loc[ope_date])  # 做多这个小数
                bit_long = True
                # print('bit_long')

            elif gold_pc.loc[ope_date] < bit_pc.loc[ope_date]:
                # if man.is_short('bitcoin'):
                #     man.short_close('bitcoin', self.bitcoin.loc[ope_date])
                # elif man.is_short('gold'):
                #     man.short_close('gold', self.gold.loc[ope_date])
                # elif man.is_long('bitcoin'):
                #     man.long_close('bitcoin', self.bitcoin.loc[ope_date])
                man.long_open('gold', self.gold.loc[ope_date])
                gold_long = True
                # print('gold long ')

            # 强制止损
            waiting_stop = pst.loc[ope_date + 1:]
            if gold_long:
                for i in waiting_stop.index:
                    if pst.loc[ope_date] > 0 and pst.loc[i] > pst.loc[ope_date] + 1:
                        [money, profit] = man.long_close('gold', self.gold.loc[i])

                        gold_long = False
                    elif pst.loc[ope_date] < 0 and pst.loc[i] < pst.loc[ope_date] - 1:
                        [money, profit] = man.long_close('gold', self.gold.loc[i])

                        gold_long = False

            elif bit_long:
                for i in waiting_stop.index:
                    if pst.loc[ope_date] > 0 and pst.loc[i] > pst.loc[ope_date] + 1:
                        [money, profit] = man.long_close('bitcoin', self.bitcoin.loc[i])

                        bit_long = False
                    elif pst.loc[ope_date] < 0 and pst.loc[i] < pst.loc[ope_date] - 1:
                        [money, profit] = man.long_close('bitcoin', self.bitcoin.loc[i])

                        bit_long = False

            # 正常平仓
            if gold_long:
                value = self.gold.loc[self.del_date_end]
                [money, profit] = man.long_close('gold', value)

                gold_long = False

            elif bit_long:
                value = self.bitcoin.loc[self.del_date_end]
                [money, profit] = man.long_close('bitcoin', value)

                bit_long = False
        return [money, profit]


if __name__ == '__main__':
    date = pd.read_excel('Value_BitAndGoal.xlsx')
    bitcoin = date['Value'].rename('bitcoin')
    gold = date['USD (PM)'].rename('gold')
    man = Action()

    moneys = []
    profits = []
    del_date_ends = []
    for i in range(19):
        num = int(85 + (i + 1) * 60)
        del_date_ends.append(num)
    del_date_ends.append(int(1265))
    del_date_ends = np.array(del_date_ends)
    obs_date_ends = del_date_ends - 60

    for i in range(len(del_date_ends)):
        # print('Pairs %s' % (i + 1))
        obs_date_end = obs_date_ends[i]
        del_date_end = del_date_ends[i]
        pairs = Pairs(gold, bitcoin, obs_date_end, del_date_end)
        [money, profit] = pairs.open_and_close(man)
        moneys.append(money)
        profits.append(profit)
    from matplotlib import pyplot as plt

    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()
    ax.plot(moneys)
    plt.figure(dpi=600)
    ax.set(xlabel='Times', ylabel='Wallet',
           title='Only Pairs')
    ax.grid()
    fig.savefig("test.png", bbox_inches='tight')
    plt.show()
