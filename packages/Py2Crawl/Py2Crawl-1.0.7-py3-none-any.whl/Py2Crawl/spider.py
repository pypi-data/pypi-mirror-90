from typing import Union
from Py2Crawl.middleware.req_res_middleware import ReqResMiddleware
from Py2Crawl.utils.request import Request
from Py2Crawl.utils.response import Response
from Py2Crawl.http.methods import Py2CrawlMethods
from Py2Crawl.utils.logger import LOGGER


class Py2CrawlSpider:
    def __init__(
            self, start_urls: list, start_urls_method: Py2CrawlMethods, callback, q_app,
            start_script: Union[str, list] = "", *args, **kwargs
    ):
        LOGGER.info("Initialize Spider")
        self.start_urls: list = start_urls
        self.start_script = start_script
        self.callback = callback
        self.start_urls_method = start_urls_method
        self.crawled = []
        self.req_res = ReqResMiddleware()
        self.q_app = q_app

    async def execute(self, request: Request, *args, **kwargs):
        if str(request.url) in self.crawled:
            return
        LOGGER.info(f"Crawling site: {str(request.url)}")
        res: Response = await self.req_res.process(request)
        self.crawled.append(str(res.url))
        await self._from_crawler(res, *args, **kwargs)

    async def _from_crawler(self, response: Response, *args, **kwargs):
        await self.callback(response, *args, **kwargs)

    async def start_crawler(self, *args, **kwargs):
        for i in self.start_urls:
            r = Request(
                url=i,
                method=self.start_urls_method,
                script=self.start_script
            )
            await self.execute(r, *args, **kwargs)
