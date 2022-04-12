import pandas as pd
import talib
from statsmodels.tsa.stattools import adfuller


def get_macd(close):
    """close - 收盘价，ndarray, shape=(n,) {data.reshape(-1)}"""
    # macd会因为数据存在nan而返回大量nan
    [dif, dea, macd] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)  # 这里的参数可以继续优化
    test = macd[pd.notnull(macd)]  # 提取非NAN值
    result = adfuller(test)  # ADF平稳检验
    info = {'DIF': dif, 'DEA': dea, 'MACD': macd, 'ATF': [result]}  # 通过这个观察已经很平稳了
    return info


def get_macd_signal(macd, date_now, signal=0, reset=False):
    """输入当前日期及对应信号，根据当前macd
    macd -- macd 值
    signal -- 交易操作信号
    date_now -- 当前日期
    """
    date_before = date_now - 1

    if macd[date_now] > 0 > macd[date_before]:
        signal = 1  # 进入多头市场，价格看涨
        # 建多头仓
        # 平空头仓
    elif macd[date_now] < 0 < macd[date_before]:
        signal = -1  # 进入空头市场，价格看跌
        # 建空头仓
        # 平多头仓
    return signal
