from scrapy.utils.project import get_project_settings
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner

from ir_project_1.spiders.spidi import SpidiSpider

runner = CrawlerRunner(get_project_settings())
task = LoopingCall(lambda: runner.crawl(SpidiSpider))
task.start(6 * 60 * 60)
reactor.run()
