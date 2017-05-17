# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LawyersItem(scrapy.Item):
    name = scrapy.Field()
    barnum = scrapy.Field()
    status = scrapy.Field()
    firmname = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    mail = scrapy.Field()
