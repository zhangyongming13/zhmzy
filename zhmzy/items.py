# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhmzyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tiezi_name = scrapy.Field()
    tiezi_link = scrapy.Field()
    tupian_link = scrapy.Field()
