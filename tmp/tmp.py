#!/usr/bin/python
#-*- coding:utf-8 -*-

import inc
import logging


global_logger = logging.getLogger('global')
log_level = 40
global_logger.setLevel(log_level)

global_fh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s -- %(message)s')
global_fh.setFormatter(formatter)

global_logger.addHandler(global_fh)

global_logger.debug("debug message")  
global_logger.info("info message")  
global_logger.warn("warn message")  
global_logger.error("error message")  
global_logger.critical("critical message")
