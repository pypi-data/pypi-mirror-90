import talib as ta
import numpy as np
import pandas as pd

from cy_components.defines.column_names import *
from .base import BaseExchangeStrategy

COL_STD = 'std'
COL_MEDIAN = 'median'
COL_UPPER = 'upper'
COL_LOWER = 'lower'
COL_SIGNAL_LONG = 'signal_long'
COL_SIGNAL_SHORT = 'signal_short'
COL_PRE_SIGNAL = 'pre_signal'
COL_RSI = 'rsi'


class BollingExchangeStrategy(BaseExchangeStrategy):
    """布林线交易策略"""
    m = 0
    n = 0
    rsi_period = 0
    rsi_threshold = 0
    open_deviate_threshold = 1.0  # 开仓偏移比例阈值，低于这个比例值才真实开仓，默认 1.0，即不在乎

    def __init__(self, *args, **kwargs):
        """m: Scale; n: Period; rsi_period/rsi_threshold; open_deviate_threshold;"""
        super(BollingExchangeStrategy, self).__init__(args, kwargs)
        self.m = round(self.m, 4)
        self.open_deviate_threshold = round(self.open_deviate_threshold, 4)

    def __str__(self):
        return 'bolling_strategy'

    @classmethod
    def strategy_with(cls, parameters):
        bolling = BollingExchangeStrategy()
        bolling.m = parameters[0]
        bolling.n = parameters[1]
        bolling.rsi_period = parameters[2]
        bolling.rsi_threshold = parameters[3]
        bolling.open_deviate_threshold = parameters[4]
        return bolling

    @property
    def identifier(self):
        res_str = '| m: %s | n: %s' % (self.m, self.n)
        if self.leverage != 1:
            res_str = res_str + ' | leverage: {}'.format(self.leverage)
        if self.rsi_period > 0:
            res_str = res_str + ' | rsi_period: {} | rsi_threshold: {}'.format(self.rsi_period, self.rsi_threshold)
        if self.open_deviate_threshold < 1:
            res_str = res_str + ' | open_threshold: {}'.format(self.open_deviate_threshold)
        res_str = res_str + ' |'
        return res_str

    @property
    def name(self):
        return "Bolling"

    @property
    def candle_count_for_calculating(self):
        """多取10个以防万一"""
        return self.n + 10

    def available_to_calculate(self, df: pd.DataFrame):
        return self.m > 0 and self.n > 0 and df.shape[0] > self.m

    def calculate_signals(self, df: pd.DataFrame, drop_extra_columns=True):
        #         print("""
        # Bolling Parameters：
        #     m: %s
        #     n: %s
        #     l: %s
        #   rsi: %s
        # rsi_t: %s
        #         """ % (str(self.m), str(self.n), str(self.leverage), str(self.rsi_period), str(self.rsi_threshold)))
        m = self.m
        n = self.n
        rsi_period = self.rsi_period
        rsi_threshold = self.rsi_threshold
        # 计算均线
        df[COL_MEDIAN] = ta.MA(df[COL_CLOSE], timeperiod=n)

        # 计算上轨、下轨道
        df[COL_STD] = ta.STDDEV(df[COL_CLOSE], timeperiod=n, nbdev=1)  # ddof代表标准差自由度
        df[COL_UPPER] = df[COL_MEDIAN] + m * df[COL_STD]
        df[COL_LOWER] = df[COL_MEDIAN] - m * df[COL_STD]
        # 趋势强度
        if rsi_period > 0:
            df[COL_RSI] = ta.RSI(df[COL_CLOSE], timeperiod=rsi_period)
        else:
            df[COL_RSI] = 100

        # ===找出做多平仓信号
        condition1 = df[COL_CLOSE] < df[COL_MEDIAN]  # 当前K线的收盘价 < 中轨
        condition2 = df[COL_CLOSE].shift(1) >= df[COL_MEDIAN].shift(1)  # 之前K线的收盘价 >= 中轨
        df.loc[condition1 & condition2, COL_SIGNAL_LONG] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

        # ===找出做多信号
        condition1 = df[COL_CLOSE] > df[COL_UPPER]  # 当前K线的收盘价 > 上轨
        condition2 = df[COL_CLOSE].shift(1) <= df[COL_UPPER].shift(1)  # 之前K线的收盘价 <= 上轨
        condition3 = df[COL_RSI] > rsi_threshold   # 趋势强度超过阙值
        df.loc[condition1 & condition2 & condition3, COL_SIGNAL_LONG] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

        if self.shortable:
            # ===找出做空平仓信号
            condition1 = df[COL_CLOSE] > df[COL_MEDIAN]  # 当前K线的收盘价 > 中轨
            condition2 = df[COL_CLOSE].shift(1) <= df[COL_MEDIAN].shift(1)  # 之前K线的收盘价 <= 中轨
            df.loc[condition1 & condition2, COL_SIGNAL_SHORT] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

            # ===找出做空信号
            condition1 = df[COL_CLOSE] < df[COL_LOWER]  # 当前K线的收盘价 < 下轨
            condition2 = df[COL_CLOSE].shift(1) >= df[COL_LOWER].shift(1)  # 之前K线的收盘价 >= 下轨
            df.loc[condition1 & condition2 & condition3, COL_SIGNAL_SHORT] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空
            # df.drop_duplicates(subset=[COL_SIGNAL_LONG, COL_SIGNAL_SHORT], inplace=True)
        else:
            df[COL_SIGNAL_SHORT] = np.nan

        # ===合并做多做空信号，去除重复信号
        df[COL_SIGNAL] = df[[COL_SIGNAL_LONG, COL_SIGNAL_SHORT]].sum(axis=1, min_count=1, skipna=True)

        # ===填空，周期用时间标记
        df.signal.fillna(method='ffill', inplace=True)
        df.loc[df.signal != df.shift(1).signal, 'start_time'] = df.candle_begin_time
        df.start_time.fillna(method='ffill', inplace=True)
        grouped = df.groupby('start_time')

        def real_signal(df):
            if df.shape[0] == 1:
                df['real_signal'] = df.signal
                return df
            off_percent = self.open_deviate_threshold
            condition_1 = df.signal.notnull()
            condition_2_1 = (df.signal > 0) & ((df.shift(-1)[COL_OPEN] / df.shift(-1)[COL_MEDIAN]) < (1 + off_percent))
            condition_2_2 = (df.signal < 0) & ((df.shift(-1)[COL_OPEN] / df.shift(-1)[COL_MEDIAN]) > (1 - off_percent))
            condition_2_3 = df.signal == 0
            df.loc[condition_1 & (condition_2_1 | condition_2_2 | condition_2_3), 'real_signal'] = df.signal
            return df
        # === 计算真实开仓点
        df = grouped.apply(real_signal).fillna(method='ffill')

        # # === 去除重复信号
        df.loc[df.real_signal.notnull() & (df.real_signal != df.real_signal.shift(1)), 'tmp_signal'] = df.real_signal
        df[COL_SIGNAL] = df['tmp_signal']
        if drop_extra_columns:
            df.drop([COL_MEDIAN, COL_STD, COL_UPPER, COL_LOWER, COL_SIGNAL_LONG,
                     COL_SIGNAL_SHORT, COL_RSI, 'real_signal', 'start_time', 'tmp_signal'], axis=1, inplace=True)

        return df

    def calculate_realtime_signals(self, df, avg_price, debug=False):
        return self.calculate_signals(df).iloc[-1].signal
