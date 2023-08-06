from typing import Union
from Py2Crawl.http.methods import Py2CrawlMethods
from Py2Crawl.http.pwb_http import Py2WebRequest
from Py2Crawl.http.a_http import AsyncHttpRequest
from Py2Crawl.exceptions import InvalidMethod
from Py2Crawl.utils.input_validation import valid_url


class Request:
    def __init__(self,
                 url: str,
                 method: Py2CrawlMethods,
                 params: dict = None,
                 data: dict = None,
                 json: dict = None,
                 redirect: bool = True,
                 script: Union[str, list] = "",
                 wait_bs: int = 0,
                 wait_as: int = 0,
                 cookies=None
                 ):
        self.url = valid_url(url)
        self.method = method
        self.redirect = redirect
        self.params = params
        self.data = data
        self.json = json
        self.script = script
        self.wait_bs = wait_bs,
        self.wait_as = wait_as,
        self.cookies = cookies

    async def execute(self):
        if self.method == Py2CrawlMethods.PW_GET:
            return await Py2WebRequest().get(
                url=self.url, script=self.script, wait_bs=self.wait_bs[0], wait_as=self.wait_as[0], cookies=self.cookies
            )
        elif self.method == Py2CrawlMethods.AH_GET:
            return await AsyncHttpRequest().get(url=self.url, redirect=self.redirect, params=self.params)
        elif self.method == Py2CrawlMethods.AH_POST:
            return await AsyncHttpRequest().post(url=self.url, data=self.data, json=self.json)
        elif self.method == Py2CrawlMethods.AH_PUT:
            return await AsyncHttpRequest().put(url=self.url, data=self.data)
        elif self.method == Py2CrawlMethods.AH_DELETE:
            return await AsyncHttpRequest().delete(url=self.url)
        elif self.method == Py2CrawlMethods.AH_HEAD:
            return await AsyncHttpRequest().head(url=self.url, redirect=self.redirect)
        elif self.method == Py2CrawlMethods.AH_OPTIONS:
            return await AsyncHttpRequest().options(url=self.url, redirect=self.redirect)
        elif self.method == Py2CrawlMethods.AH_PATCH:
            return await AsyncHttpRequest().patch(url=self.url, data=self.data)
        else:
            raise InvalidMethod(self.method)
