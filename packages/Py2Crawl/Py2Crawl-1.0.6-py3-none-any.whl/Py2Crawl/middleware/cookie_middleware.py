class CookieMiddleware:
    def __init__(self):
        self.ah_cookie_store = []
        self.p2w_cookie_store = []

    async def add_ah_cookie(self, cookie: dict):
        self.ah_cookie_store.append(cookie)

    async def delete_ah_cookie(self, cookie: dict):
        self.ah_cookie_store.remove(cookie)

    async def get_ah_cookie(self):
        return self.ah_cookie_store

    async def add_p2w_cookie(self, cookie: dict):
        self.p2w_cookie_store.append(cookie)

    async def delete_p2w_cookie(self, cookie: dict):
        self.p2w_cookie_store.remove(cookie)

    async def get_p2w_cookie(self):
        return self.p2w_cookie_store
