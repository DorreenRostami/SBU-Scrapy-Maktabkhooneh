import re
import sys

import scrapy

from db.db import DB
from ir_project_1.items import CourseItem


class SpidiSpider(scrapy.Spider):
    name = 'spidi'
    allowed_domains = ['maktabkhooneh.org']
    start_urls = ['http://maktabkhooneh.org/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DB('sqlite3.db')

    def parse(self, response, **kwargs):
        print("Starting parse operation")
        items = get_by_class(response, "div", "course-card")
        for index, item in enumerate(items):
            data_url = response.urljoin(item.xpath("@data-url").get())
            relative_link = get(get_by_class(item, "a", "course-card__wrapper", "/@href"))
            link = response.urljoin(relative_link)
            idPattern = re.search('course/(.+)/extra', data_url)
            if idPattern is None:
                continue
            course = {
                'id': idPattern.group(1),
                'title': get_by_class(item, "div", "course-card__title", "/text()").get(),
                'link': link,
            }
            if course['title'] == "" or course['title'] is None:
                continue

            yield scrapy.Request(
                data_url,
                callback=self.parse_data_url,
                cb_kwargs={'course': course, 'link': link},
            )

    def parse_data_url(self, response, **kwargs):
        course = kwargs['course']
        extra_time = get_by_class(response, "div", "course-card-extra__time")
        duration = get_by_class(extra_time, "div", "course-card-extra__header", "/text()")
        course['duration'] = get(duration[1])
        course['instructor'] = get(
            response.xpath('//div[@class="filler space-between"]/div[@class="color-gunmetal"]/span/a/text()'))
        course['organizer'] = response.xpath('//div[@class="filler space-between"]/div[@class="color-gunmetal"]/span')[
            0].xpath('text()').get()
        course['price'] = get(response.xpath('//div[@class="course-card-extra__price"]/text()'), 'free')
        link = kwargs['link']
        yield scrapy.Request(
            link,
            callback=self.parse_details_page,
            cb_kwargs={'course': course, 'link': link},
        )

    def parse_details_page(self, response, **kwargs):
        course = kwargs['course']
        course['description'] = ''.join(
            element.xpath('text()').get() if len(element.xpath('text()')) > 0 else '' for element
            in get_by_class(response, "div", "js-shortened__content").xpath('*'))
        course['satisfaction'] = get(get_by_class(response, "span", "course-intro__rate-value", "/text()"))
        self.db.create_course(course_to_list(course))
        yield CourseItem(course)


def get_by_class(response, el, class_name, additional_query=""):
    return response.xpath(
        ".//" + el + "[contains(concat(' ', normalize-space(@class), ' '), ' " + class_name + " ')]" + additional_query)


def get(selector, default=''):
    value = selector.get()
    if value:
        return value.strip('\n').strip()
    return default


def course_to_list(course):
    return [
        course['id'],
        course['title'],
        course['duration'],
        course['instructor'],
        course['organizer'],
        course['price'],
        course['link'],
        course['satisfaction'],
        course['description']
    ]


