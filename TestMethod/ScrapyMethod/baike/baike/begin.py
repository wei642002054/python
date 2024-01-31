# -*- coding: utf-8 -*-
import multiprocessing
from scrapy import cmdline
from scrapy.utils.project import get_project_settings
spider_name = 'mybaike'
cmdline.execute("scrapy crawl {0}".format(spider_name).split(' '))
