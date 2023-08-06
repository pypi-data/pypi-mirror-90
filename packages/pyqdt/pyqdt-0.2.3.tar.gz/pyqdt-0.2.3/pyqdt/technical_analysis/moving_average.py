# -*- coding: utf-8 -*-
# 均线指标

from .arithmetic import *


@arithmetic_wrapper
def HMA(N=12):
    """高价平均线

    公式：
        HMA: MA(HIGH, N)
    输入：
        N：统计的天数
    输出：
        HMA: 最高价的N日简单移动平均
    """
    return MA(HIGH, N)


@arithmetic_wrapper
def LMA(N=12):
    """低价平均线

    公式：
        LMA: MA(LOW, N)
    输入：
        N：统计的天数
    输出:
        LMA: 最低价的N日简单移动平均
    """
    return MA(LOW, N)


@arithmetic_wrapper
def VMA(N=12):
    """变异平均线

    公式：
        V:=(HIGH+OPEN+LOW+CLOSE)/4
        VMA:MA(VV,N)
    输入：
        N：统计的天数
    输出：
        VMA: VV的N日简单移动平均。
    """
    V = (HIGH + OPEN + LOW + CLOSE) / 4
    return MA(V, N)


@arithmetic_wrapper
def EXPMA(N=12):
    """指数平均线

    公式：
        EXPMA:EMA(CLOSE,N)
    输入：
        N：统计的天数
    输出：
        EXPMA
    """
    return EMA(**locals())
