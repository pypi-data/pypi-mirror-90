# -*- coding: utf-8 -*-
# 成交量型指标

from .arithmetic import *


@arithmetic_wrapper
def OBV():
    """累计能量线

    公式：
        VA = 如果收盘价>1日前的收盘价,返回成交量(手),否则返回-成交量(手)
        OBV = 如果收盘价=1日前的收盘价,返回0,否则返回VA的历史累和
    输出：
        OBV
    """
    return SUM(IF(CLOSE > REF(CLOSE, 1), VOL, IF(CLOSE < REF(CLOSE, 1), -VOL, 0)), 0)
