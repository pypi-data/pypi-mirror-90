# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DetailScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    main_category = scrapy.Field()
    sub_category = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()

