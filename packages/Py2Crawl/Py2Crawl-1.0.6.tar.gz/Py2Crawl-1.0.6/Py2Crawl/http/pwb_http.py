from typing import Union
from Py2Web.main import get as pw_get


class Py2WebRequest:
    @classmethod
    async def get(cls, url: str, script: Union[str, list] = "", wait_bs: int = 0, wait_as: int = 0, cookies=None):
        res = pw_get(url=url, script=script, wait_bs=wait_bs, wait_as=wait_as, cookies=cookies)
        return dict(res)
