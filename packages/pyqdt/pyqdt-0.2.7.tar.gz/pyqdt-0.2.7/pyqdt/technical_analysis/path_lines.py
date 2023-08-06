# -*- coding: utf-8 -*-
# 路径型指标
from .arithmetic import *

@arithmetic_wrapper
def BOLL(M=20, B=2):
    """布林带

    公式：
        MB:MA(CLOSE,M);
        UB:MID+N*STD(CLOSE,M);
        LB:MID-N*STD(CLOSE,M);
    输入：
        M：统计的天数 M
        B：布林带宽度 B
    输出：
        中轨线MB，上轨线UB、下轨线LB
    定义：
        RETURNS=(BOLL, UB, LB)

    """
    MB = MA(CLOSE, M)
    UB = MB + B * STD(CLOSE, M)
    LB = MB - B * STD(CLOSE, M)
    return MB, UB, LB