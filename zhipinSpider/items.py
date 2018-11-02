# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class ZhipinspiderItem(Item):

    job = Field()
    salary = Field()
    company_name = Field
    address = Field()
    require = Field()
    company_size = Field()
    job_info = Field()
    company_info = Field()