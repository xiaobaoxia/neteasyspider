# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NeteasymusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    artists_name = scrapy.Field()
    album_name = scrapy.Field()
    total = scrapy.Field()
    id = scrapy.Field()


class CommentItem(scrapy.Item):
    music_id = scrapy.Field()
    comment = scrapy.Field()
    nickname = scrapy.Field()
    time = scrapy.Field()
    likedcount = scrapy.Field()
    id = scrapy.Field()