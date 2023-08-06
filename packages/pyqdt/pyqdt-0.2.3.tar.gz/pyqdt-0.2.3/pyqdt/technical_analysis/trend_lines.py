# -*- coding: utf-8 -*-
# 趋势指标
from .arithmetic import *


@arithmetic_wrapper
def MACD(X=CLOSE, SHORT=12, LONG=26, MID=9):
    """
    公式：
        DIF:EMA(CLOSE,SHORT)-EMA(CLOSE,LONG);
        DEA:EMA(DIF,MID);
        MACD:(DIF-DEA)*2,COLORSTICK;
        输出DIF = 收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
        输出DEA = DIF的MID日指数移动平均
        输出平滑异同平均 = (DIF-DEA)*2,COLORSTICK
    输入：
        SHORT：统计的天数 SHORT
        LONG：统计的天数 LONG
        MID：统计的天数 MID
    输出：
        RETURNS=(DIF, DEA, MACD)
    """
    DIF = EMA(X, SHORT) - EMA(X, LONG)
    DEA = EMA(DIF, MID)
    MACD = (DIF - DEA) * 2
    return DIF, DEA, MACD


@arithmetic_wrapper
def VMACD(SHORT=12, LONG=26, MID=9):
    """
    公式：
        DIF:EMA(VOL,SHORT)-EMA(VOL,LONG);
        DEA:EMA(DIF,MID);
        MACD:DIF-DEA,COLORSTICK;
        输出DIF:成交量(手)的SHORT日指数移动平均-成交量(手)的LONG日指数移动平均
        输出DEA:DIF的MID日指数移动平均
        输出平滑异同平均:DIF-DEA,COLORSTICK
    输入：
        SHORT：统计的天数 SHORT
        LONG：统计的天数 LONG
        MID：统计的天数 MID
    输出：
        RETURNS=(DIF, DEA, MACD)
    """
    DIF = EMA(VOL, SHORT) - EMA(VOL, LONG)
    DEA = EMA(DIF, MID)
    MACD = DIF - DEA
    return DIF, DEA, MACD


@arithmetic_wrapper
def QACD(N1=12, N2=26, M=9):
    """
    公式：
        DIF:EMA(CLOSE,N1)-EMA(CLOSE,N2);
        MACD:EMA(DIF,M);
        DDIF:DIF-MACD;
        输出DIF = 收盘价的N1日指数移动平均-收盘价的N2日指数移动平均
        输出平滑异同平均 = DIF的M日指数移动平均
        输出DDIF = DIF-MACD
    输入：
        N1：统计的天数 N1
        N2：统计的天数 N2
        M：统计的天数 M
    输出：
        RETURNS=(DIF, MACD, DDIF)
    """
    DIF = EMA(CLOSE, N1) - EMA(CLOSE, N2)
    MACD = EMA(DIF, M)
    DDIF = DIF - MACD
    return DIF, MACD, DDIF
