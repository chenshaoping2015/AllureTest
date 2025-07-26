# -*- coding:utf-8 -*-
# @Time  :2022/11/10 0:12
# @Author: stevenchen
import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

from utils.path_utils import PathUtils


class Singleton(type):
    """
    单例模式元类实现
    作用：确保每个类只有一个实例存在
    特性：
     - 支持多线程环境
     - 自动管理实例生命周期
     - 兼容类继承结构
    """
    _instances = {}  # 类级字典，存储所有单例类的唯一实例
    
    def __call__(cls, *args, **kwargs):
        """重写实例化行为"""
        if cls not in cls._instances:
            # 调用父类元类的__call__方法实际创建实例
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logging(metaclass=Singleton):
    # 设置log文件名称
    def __init__(self):
        # 创建日志文件夹
        self.log_path = PathUtils().directory('log')
        # 创建日志文件名称：当前日期.log    
        self.filename = f"{time.strftime("%Y-%m-%d", time.localtime())}.log"
        # 拼接日志文件路径：日志文件夹路径 + 日志文件名称
        self.filename = os.path.join(self.log_path, self.filename)
        # 规范化日志文件路径
        self.filename = os.path.normpath(self.filename)

    # 生成日志的主方法,传入对那些级别及以上的日志进行处理
    def get_logger(self):
        """logger 是通过自身携带的 handler 来输出日志的，例如 StreamHandler（向终端输出日志）和 FileHandler（向文件输出日志）"""
        # 创建日志器
        logger = logging.getLogger(__name__)
        # 设置日志的打印级别
        logger.setLevel(logging.INFO)
        # 防止重新生成处理器
        if not logger.handlers:
            # 创建日志处理器，向终端输出日志
            sh = logging.StreamHandler()
            # 每天重新创建一个日志文件，最多保留5份
            fh = TimedRotatingFileHandler(filename=self.filename, when='midnight', interval=1, backupCount=5, encoding='utf-8')
            # 创建日志文件格式器
            fmt = logging.Formatter("[%(asctime).19s] %(process)d:%(levelname).1s %(filename)s:%(lineno)d:%(funcName)s: %(message)s")
            # 给处理器添加格式
            sh.setFormatter(fmt=fmt)
            fh.setFormatter(fmt=fmt)
            # 给日志器添加处理器，过滤器一般在工作中用的比较少，如果需要精确过滤，可以使用过滤器
            logger.addHandler(sh)
            logger.addHandler(fh)
        return logger
