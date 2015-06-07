#!/usr/bin/python
#-*- coding:utf-8 -*-

import widget
import logging
import dbm
import ConfigParser

cf,dbm,logger = widget.getfiles('getOracle')
logger.info('hahhahahsdlfkhaslkdjfhalskdjf')
print cf.get('xuniji','tnsname')
