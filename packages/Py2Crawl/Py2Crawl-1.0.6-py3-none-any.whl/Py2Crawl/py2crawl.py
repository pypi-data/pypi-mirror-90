from Py2Crawl.settings.base_settings import BaseSettings
from Py2Crawl.spider import Py2CrawlSpider
from Py2Crawl.utils.logger import LOGGER


class Py2Crawl:
    def __int__(self, settings=BaseSettings()):
        LOGGER.info("Initialize Py2Crawl class")
        self.settings = settings

    async def crawl(self, spider: Py2CrawlSpider, *args, **kwargs):
        LOGGER.info("Start crawling")
        await spider.start_crawler(*args, **kwargs)
