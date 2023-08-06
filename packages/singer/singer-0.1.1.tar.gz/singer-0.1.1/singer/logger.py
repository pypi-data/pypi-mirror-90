# coding=utf-8
import logging


# %(levelno)s: 打印日志级别的数值
# %(levelname)s: 打印日志级别名称
# %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
# %(filename)s: 打印当前执行程序名
# %(funcName)s: 打印日志的当前函数
# %(lineno)d: 打印日志的当前行号
# %(asctime)s: 打印日志的时间
# %(thread)d: 打印线程ID
# %(threadName)s: 打印线程名称
# %(process)d: 打印进程ID
# %(message)s: 打印日志信息
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(threadName)s [%(name)s] %(message)s')


def logger(name='', level=logging.DEBUG):
    '''获取日志记录器
    '''
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
