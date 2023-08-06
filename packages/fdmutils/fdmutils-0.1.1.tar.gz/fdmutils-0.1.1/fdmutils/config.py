#coding=utf-8
import io
import traceback
import json
import math
import pandas
import configparser
import logging
from logging import handlers
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from common import get_tb_info
from common import debug_line

class LogLevelFilter(logging.Filter):
    def __init__(self, name='', level=logging.DEBUG):
        super(LogLevelFilter,self).__init__(name)
        self.level = level

    def filter(self, record):
        return record.levelno == self.level
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
## 函数部分
## init_log_from_config     从配置文件中，获取日志配置。【特殊参数_root_dir】
## read_config              从配置文件中，获取需要解析的特征
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def init_log_from_config(_config_path,_root_dir=""):
    msg     = "success"
    flag    = 0
    logger  = None
    try:
        config = configparser.ConfigParser()
        config.read(_config_path)

        module      = config.get('log','module',raw=True)
        base_dir    = config.get('log','base',raw=True).format(ROOT_DIR=_root_dir)
        pout_info   = os.path.join(base_dir,config.get('log','info',raw=True))
        pout_debug  = os.path.join(base_dir,config.get('log','debug',raw=True))
        pout_error  = os.path.join(base_dir,config.get('log','error',raw=True))

        logger = logging.getLogger(module)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s",datefmt="%Y-%m-%d %H:%M:%S")

        fh_info  = handlers.TimedRotatingFileHandler(pout_info, when="midnight", interval=1, backupCount=3)
        fh_info.setLevel(logging.INFO)
        fh_debug = handlers.TimedRotatingFileHandler(pout_debug, when="midnight", interval=1, backupCount=3)
        fh_debug.setLevel(logging.DEBUG)
        fh_error = handlers.TimedRotatingFileHandler(pout_error, when="midnight", interval=1, backupCount=3)
        fh_error.setLevel(logging.ERROR)

        filter_info  = LogLevelFilter(level=logging.INFO)
        filter_debug = LogLevelFilter(level=logging.DEBUG)
        filter_error = LogLevelFilter(level=logging.ERROR)

        fh_info.addFilter(filter_info)
        fh_debug.addFilter(filter_debug)
        fh_error.addFilter(filter_error)
        fh_info.setFormatter(formatter)
        fh_debug.setFormatter(formatter)
        fh_error.setFormatter(formatter)

        logger.addHandler(fh_info)
        logger.addHandler(fh_debug)
        logger.addHandler(fh_error)
    except:
        msg     = get_tb_info()
        flag    = -1
        logger  = None

    return msg,flag,logger

def read_config(_config_path):
    msg     = "success"
    flag    = 0
    config  = None
    try:
        config = configparser.ConfigParser()
        config.read(_config_path)
    except:
        msg     = get_tb_info()
        flag    = -1
        config  = None
    return msg,flag,config

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
## 变量部分
## logger               ##打印日志的全局变量，从log.conf中解析 
## config               ##特征配置的全局变量，从feature.conf中解析 
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""
CURRENT_DIR     = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR        = os.path.join(CURRENT_DIR, '../../')
CONFIG_LOG      = os.path.join(ROOT_DIR,"conf/log.conf")
CONFIG_FEATURE  = os.path.join(ROOT_DIR,"conf/feature.conf")
msg,flag,logger = init_log_from_config(CONFIG_LOG,_root_dir=ROOT_DIR)
msg,flag,config = read_config(CONFIG_FEATURE)
"""


