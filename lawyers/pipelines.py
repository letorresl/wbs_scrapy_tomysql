# -*- coding: utf-8 -*-

import pymysql
import ConfigParser


class LawyersPipeline(object):


    def open_spider(self, spider):
        # Read MySQL config
        config = ConfigParser.ConfigParser()
        config.read('mysql.cfg')
        # Connect to database using params from the config file
        self.conn = pymysql.connect(
            host= config.get('connection', 'host'),
            port= config.getint('connection', 'port'),
            user= config.get('credentials', 'user'),
            passwd= config.get('credentials', 'password'),
            db= config.get('output', 'database'),
            charset= 'utf8'
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute(
            "INSERT IGNORE INTO lawyers VALUES " +\
            "(%(name)s, %(barnum)s, %(status)s, " +\
            "%(firmname)s, %(address)s, %(phone)s, " +\
            "%(mail)s);",
            dict(item)
        )
        self.conn.commit()
