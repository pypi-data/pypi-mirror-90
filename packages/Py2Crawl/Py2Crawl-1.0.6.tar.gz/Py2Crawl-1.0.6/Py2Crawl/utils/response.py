class Response:
    def __init__(self, url: str, content: str, cookies: dict = None, js_response: any = None, process_time: any = None):
        self.url = url
        self.content = content
        self.cookies = cookies
        self.js_response = js_response
        self.process_time = process_time
