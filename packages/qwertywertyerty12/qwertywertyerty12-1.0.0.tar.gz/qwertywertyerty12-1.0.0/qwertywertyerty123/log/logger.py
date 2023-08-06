from O2DESPy.application.config import Config
import logging.handlers
import sys
import os
import datetime
import logging

sys.path.append('../../')


class Logger(object):
    level_switch = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    logger = logging.getLogger("logger")
    stream_handler = None
    file_handler = None

    debug_sign = True
    info_sign = True
    warning_sign = True
    error_sign = True
    critical_sign = True

    def __init__(self,
                 file_path=Config.log_file_path,
                 stream_level='debug',
                 file_level='debug',
                 output_mode=None,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):

        if output_mode is None:
            output_mode = ['stream', 'file']
        self.update_config(file_path=file_path, stream_level=stream_level, file_level=file_level,
                           output_mode=output_mode, fmt=fmt)

    @classmethod
    def debug(cls, *args, **kwargs):
        if cls.debug_sign:
            cls.logger.debug(*args, **kwargs)

    @classmethod
    def info(cls, *args, **kwargs):
        if cls.info_sign:
            cls.logger.info(*args, **kwargs)

    @classmethod
    def warning(cls, *args, **kwargs):
        if cls.warning_sign:
            cls.logger.warning(*args, **kwargs)

    @classmethod
    def error(cls, *args, **kwargs):
        if cls.error_sign:
            cls.logger.error(*args, **kwargs)

    @classmethod
    def critical(cls, *args, **kwargs):
        if cls.critical_sign:
            cls.logger.critical(*args, **kwargs)

    @classmethod
    def update_config(cls,
                      file_path=Config.log_file_path,
                      include_log=None,
                      stream_level='debug',
                      file_level='debug',
                      name = '',
                      dynamic=False,
                      output_mode=None,
                      fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):

        if output_mode is None:
            output_mode = ['stream', 'file']
        if include_log is None:
            include_log = ['debug', 'info', 'warning', 'error', 'critical']
        cls.debug_sign = True if 'debug' in include_log else False
        cls.info_sign = True if 'info' in include_log else False
        cls.warning_sign = True if 'warning' in include_log else False
        cls.error_sign = True if 'error' in include_log else False
        cls.critical_sign = True if 'critical' in include_log else False

        cls.logger.setLevel(logging.DEBUG)
        file_path = file_path
        if dynamic == True:
            file_path = os.path.join(Config.log_folder,
                                     '{}_{}.log'.format(name, datetime.datetime.now().strftime('%Y%m%d%H%M%S')))

        if 'stream' in output_mode:
            cls.stream_handler = logging.StreamHandler()
            cls.stream_handler.setLevel(cls.level_switch[stream_level])
            cls.stream_handler.setFormatter(logging.Formatter(fmt))
            cls.logger.addHandler(cls.stream_handler)
        else:
            if cls.stream_handler:
                logging.getLogger("logger").removeHandler(cls.stream_handler)
                cls.stream_handler = None

        if 'file' in output_mode:
            # mode = 'w' 会删除之前的log文件
            cls.file_handler = logging.FileHandler(filename=file_path, mode='w')
            cls.file_handler.setLevel(cls.level_switch[file_level])
            cls.file_handler.setFormatter(logging.Formatter(fmt))
            cls.logger.addHandler(cls.file_handler)
        else:
            if cls.file_handler:
                logging.getLogger("logger").removeHandler(cls.file_handler)
                cls.file_handler = None

