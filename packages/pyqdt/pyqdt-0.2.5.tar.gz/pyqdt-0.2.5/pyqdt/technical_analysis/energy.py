# -*- coding: utf-8 -*-
# 能量指标

from .arithmetic import *

@arithmetic_wrapper
def VR(N=26, M=6):
    """成交量变异率

    公式：
        TH:=SUM(IF(CLOSE>REF(CLOSE,1),VOL,0),N);
        TL:=SUM(IF(CLOSE<REF(CLOSE,1),VOL,0),N);
        TQ:=SUM(IF(CLOSE=REF(CLOSE,1),VOL,0),N);
        VR:100*(TH*2+TQ)/(TL*2+TQ);
        MAVR:MA(VR,M);
        TH赋值:如果收盘价>1日前的收盘价,返回成交量(手),否则返回0的N日累和
        TL赋值:如果收盘价<1日前的收盘价,返回成交量(手),否则返回0的N日累和
        TQ赋值:如果收盘价=1日前的收盘价,返回成交量(手),否则返回0的N日累和
        输出VR:100*(TH*2+TQ)/(TL*2+TQ)
        输出MAVR:VR的M日简单移动平均
    输入：
        N：统计的天数 N
        M：统计的天数 M
    输出：
        RETURNS=(VR, MAVR)

    """
    TH = SUM(IF(CLOSE > REF(CLOSE, 1), VOL, 0), N)
    TL = SUM(IF(CLOSE < REF(CLOSE, 1), VOL, 0), N)
    TQ = SUM(IF(CLOSE == REF(CLOSE, 1), VOL, 0), N)
    VR = 100 * (TH * 2 + TQ) / (TL * 2 + TQ)
    MAVR = MA(VR, M)
    return VR, MAVR