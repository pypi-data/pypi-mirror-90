# -*- coding: utf-8 -*-
import os
DB_URL = {'sly': 'mysql+mysqlconnector://seleya:UONw3h4Bfk0tDAMG@23.99.99.240:12306/seleya' if 'SYL_DB' not in os.environ else os.environ['SYL_DB']}

server = ('192.168.199.137', 50006, 'api.jdw.smartdata-x.top', 443)