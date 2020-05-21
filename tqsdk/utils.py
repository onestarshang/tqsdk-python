#!usr/bin/env python3
#-*- coding:utf-8 -*-
__author__ = 'yanqiong'

import datetime
import logging
import os
import random
import uuid
from functools import wraps

RD = random.Random()  # 初始化随机数引擎
DEBUG_DIR = os.path.join(os.path.expanduser('~'), ".tqsdk/logs")


def _generate_uuid(prefix=''):
    return f"{prefix + '_' if prefix else ''}{uuid.UUID(int=RD.getrandbits(128)).hex}"


def _get_log_format(is_backtest=None):
    """返回日志格式"""
    if is_backtest:
        return logging.Formatter('%(levelname)6s - %(message)s')
    else:
        return logging.Formatter('%(asctime)s - %(levelname)6s - %(message)s')


def _get_log_name():
    """返回默认 debug 文件生成的位置"""
    if not os.path.exists(DEBUG_DIR):
        os.makedirs(os.path.join(os.path.expanduser('~'), ".tqsdk/logs"), exist_ok=True)
    return os.path.join(DEBUG_DIR, f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}-{os.getpid()}.log")


def _clear_logs():
    """清除最后修改时间是 n 天前的日志"""
    if not os.path.exists(DEBUG_DIR):
        return
    n = os.getenv("TQ_SAVE_LOG_DAYS", 30)
    dt = datetime.datetime.now() - datetime.timedelta(days=int(n))
    for log in os.listdir(DEBUG_DIR):
        path = os.path.join(DEBUG_DIR, log)
        if datetime.datetime.fromtimestamp(os.stat(path).st_mtime) < dt:
            os.remove(path)


def _log_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        logging.getLogger("TqApi").debug(f'Calling [ {f.__name__}() ] with {args} {kwds}')
        return f(*args, **kwds)
    return wrapper


night_trading_table = {
    "DCE.a": ["21:00:00", "23:00:00"],
    "DCE.b": ["21:00:00", "23:00:00"],
    "DCE.c": ["21:00:00", "23:00:00"],
    "DCE.cs": ["21:00:00", "23:00:00"],
    "DCE.m": ["21:00:00", "23:00:00"],
    "DCE.y": ["21:00:00", "23:00:00"],
    "DCE.p": ["21:00:00", "23:00:00"],
    "DCE.l": ["21:00:00", "23:00:00"],
    "DCE.v": ["21:00:00", "23:00:00"],
    "DCE.pp": ["21:00:00", "23:00:00"],
    "DCE.j": ["21:00:00", "23:00:00"],
    "DCE.jm": ["21:00:00", "23:00:00"],
    "DCE.i": ["21:00:00", "23:00:00"],
    "DCE.eg": ["21:00:00", "23:00:00"],
    "DCE.eb": ["21:00:00", "23:00:00"],
    "DCE.rr": ["21:00:00", "23:00:00"],
    "DCE.pg": ["21:00:00", "23:00:00"],
    "CZCE.CF": ["21:00:00", "23:00:00"],
    "CZCE.CY": ["21:00:00", "23:00:00"],
    "CZCE.SA": ["21:00:00", "23:00:00"],
    "CZCE.SR": ["21:00:00", "23:00:00"],
    "CZCE.TA": ["21:00:00", "23:00:00"],
    "CZCE.OI": ["21:00:00", "23:00:00"],
    "CZCE.MA": ["21:00:00", "23:00:00"],
    "CZCE.FG": ["21:00:00", "23:00:00"],
    "CZCE.RM": ["21:00:00", "23:00:00"],
    "CZCE.ZC": ["21:00:00", "23:00:00"],
    "CZCE.TC": ["21:00:00", "23:00:00"],
    "SHFE.rb": ["21:00:00", "23:00:00"],
    "SHFE.hc": ["21:00:00", "23:00:00"],
    "SHFE.fu": ["21:00:00", "23:00:00"],
    "SHFE.bu": ["21:00:00", "23:00:00"],
    "SHFE.ru": ["21:00:00", "23:00:00"],
    "SHFE.sp": ["21:00:00", "23:00:00"],
    "INE.nr": ["21:00:00", "23:00:00"],
    "SHFE.cu": ["21:00:00", "25:00:00"],
    "SHFE.al": ["21:00:00", "25:00:00"],
    "SHFE.zn": ["21:00:00", "25:00:00"],
    "SHFE.pb": ["21:00:00", "25:00:00"],
    "SHFE.ni": ["21:00:00", "25:00:00"],
    "SHFE.sn": ["21:00:00", "25:00:00"],
    "SHFE.ss": ["21:00:00", "25:00:00"],
    "SHFE.au": ["21:00:00", "26:30:00"],
    "SHFE.ag": ["21:00:00", "26:30:00"],
    "INE.sc": ["21:00:00", "26:30:00"],
}


def _quotes_add_night(quotes):
    """为 quotes 中应该有夜盘但是市价合约文件中没有夜盘的品种，添加夜盘时间"""
    for symbol in quotes:
        product_id = quotes[symbol]["product_id"]
        if quotes[symbol].get("trading_time") and product_id in night_trading_table:
            quotes[symbol]["trading_time"].setdefault("night", [night_trading_table[product_id]])
