"""基础的操作"""

import numpy as np


def get_com_rate(name):
    # 获取佣金费率
    com_rate = 0
    if name == 'gold':
        com_rate = 0.01
    elif name == 'bitcoin':
        com_rate = 0.02
    return com_rate


class Action:
    def __init__(self):
        self.money = 1000  # 初始资金
        # self.dep_rate = 0.08  # 8%的保证金率
        # self.name = asset_name

        # self.gold_info = [self.gold, self.gold_long_num, self.gold_long_amo, self.gold_short_num, self.gold_short_amo]
        # self.bit_info = [self.bitcoin, self.bit_long_num, self.bit_long_amo, self.bit_short_num, self.bit_short_amo]
        self.gold_info = [0, 0, 0, 0, 0]
        self.bit_info = [0, 0, 0, 0, 0]
        self.gold = self.gold_info[0]  # 持有数量
        self.bitcoin = self.bit_info[0]
        self.gold_long_num = self.gold_info[1]
        self.gold_short_num = self.gold_info[4]
        self.bit_long_num = self.bit_info[2]
        self.bit_short_num = self.bit_info[4]
        self.gold_long_amo = self.gold_info[2]
        self.gold_short_amo = self.gold_info[3]
        self.bit_long_amo = self.bit_info[3]
        self.bit_short_amo = self.bit_info[4]

    def buy(self, name, number):
        if name == 'gold':
            self.gold += number
        elif name == 'bitcoin':
            self.bitcoin += number

    def sold(self, name, number):
        if name == 'gold':
            self.gold -= number
        elif name == 'bitcoin':
            self.bitcoin -= number

    def get_info(self, name):
        info = []
        if name == 'gold':
            info = self.gold_info
        elif name == 'bitcoin':
            info = self.bit_info
        else:
            print('name is none')
        return info

    def pass_info(self, name, info):
        # 更新info
        if name == 'gold':
            self.gold_info = info
            [self.gold, self.gold_long_num, self.gold_long_amo, self.gold_short_num,
             self.gold_short_amo] = self.gold_info
        elif name == 'bitcoin':
            self.bit_info = info
            [self.bitcoin, self.bit_long_num, self.bit_long_amo, self.bit_short_num, self.bit_short_amo] = self.bit_info

    # 在当日以收盘价进行购买
    def long_open(self, name, value):
        """做多仓
        """
        info = self.get_info(name)
        [asset_number, long_num, long_amo, short_num, short_amo] = info

        com_rate = get_com_rate(name)
        # number = floor(self.money / ((1 - self.dep_rate) + value * (com_rate + self.dep_rate)))
        number = self.money / ((1 + com_rate) * value)
        amount = value * number
        commission = amount * com_rate
        # deposit = amount * self.dep_rate

        # self.money -= (commission + deposit)
        self.money -= (commission + amount)
        # print('long open:', amount)
        # print('long number:', number)
        # print('money left:', self.money)

        asset_number += number
        long_num += number
        long_amo += amount
        info = [asset_number, long_num, long_amo, short_num, short_amo]
        self.pass_info(name, info)
        # if name == 'gold':
        # print('%s info:' % name, self.gold_info)
        # elif name == 'bitcoin':
        # print('%s info:' % name, self.bit_info)

    def long_close(self, name, value):
        """平多仓"""
        info = self.get_info(name)
        [asset_number, long_num, long_amo, short_num, short_amo] = info

        com_rate = get_com_rate(name)
        number = long_num
        amount = value * number
        commission = amount * com_rate
        profit = amount - long_amo - (commission + long_amo * com_rate)

        # self.money += (profit + (long_amo * self.dep_rate))  # 利润加保证金
        self.money += (profit + amount)
        # print('long close/sold all:', amount)
        # print('long ano', long_amo)
        # print('commission:', commission)
        # print('long com', long_amo * com_rate)
        # print('profit:', profit)
        # print('money left:', self.money)
        # print('--------------------------------------')

        asset_number -= number
        long_num = 0
        long_amo = 0
        info = [asset_number, long_num, long_amo, short_num, short_amo]
        self.pass_info(name, info)

        return [self.money, profit]

    def short_open(self, name, value):
        """做空仓"""
        info = self.get_info(name)
        [asset_number, long_num, long_amo, short_num, short_amo] = info

        com_rate = get_com_rate(name)
        number = self.money / ((1 + com_rate) * value)
        amount = value * number
        commission = amount * com_rate
        # deposit = amount * self.dep_rate

        # self.money -= (commission + deposit)
        self.money = self.money + amount - commission
        # print('short open:', amount)
        # print('short number:', number)
        # print("money left(is short):", self.money)
        # print("money left(without short):", self.money - 2 * amount)

        asset_number -= number
        short_num += number
        short_amo += amount
        info = [asset_number, long_num, long_amo, short_num, short_amo]
        self.pass_info(name, info)
        # if name == 'gold':
        # print('%s info:' % name, self.gold_info)
        # elif name == 'bitcoin':
        # print('%s info:' % name, self.bit_info)

    def short_close(self, name, value):
        """平空仓"""
        info = self.get_info(name)
        [asset_number, long_num, long_amo, short_num, short_amo] = info

        number = short_num
        com_rate = get_com_rate(name)
        amount = value * number
        commission = amount * com_rate
        profit = short_amo - amount - (commission + short_amo * com_rate)

        # self.money += (profit + short_amo * self.dep_rate)
        self.money = self.money - amount - commission
        # print('short close:', amount)
        # print('profit:', profit)
        #print('money left:', self.money)
        #print('---------------------------------------')

        asset_number += number
        short_amo = 0
        short_num = 0
        info = [asset_number, long_num, long_amo, short_num, short_amo]
        self.pass_info(name, info)

        return [self.money, profit]

    def get_money(self):
        return self.money

    def is_long(self, name):
        statu = None
        if name == 'gold':
            if np.array(self.gold_long_num).all() == 0:
                statu = False
            else:
                statu = True
        elif name == 'bitcoin':
            if np.array(self.bit_long_num).all() == 0:
                statu = False
            else:
                statu = True

        return statu

    def is_short(self, name):
        statu = True
        if name == 'gold':
            if np.array(self.gold_short_num).all() == 0:
                statu = False
            else:
                statu = True
        elif name == 'bitcoin':
            if np.array(self.bit_short_num).all() == 0:
                statu = False
            else:
                statu = True
        else:
            print('is_short wrong ')

        return statu


class Action_(Action):
    def __init__(self, money):  # 多添加一个参数
        super().__init__()
        self.money = money

    def change_money(self, number):
        self.money = number
