# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    id = scrapy.Field(serialize=str)
    title = scrapy.Field(serialize=str)
    duration = scrapy.Field(serialize=str)
    instructor = scrapy.Field(serialize=str)
    organizer = scrapy.Field(serialize=str)
    price = scrapy.Field(serialize=str)
    link = scrapy.Field(serialize=str)
    satisfaction = scrapy.Field(serialize=str)
    description = scrapy.Field(serialize=str)