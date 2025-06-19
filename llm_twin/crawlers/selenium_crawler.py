from .base import BaseSeleniumCrawler


class SeleniumCrawler(BaseSeleniumCrawler):
    def __init__(self, scroll_limit: int = 5) -> None:
        super().__init__()

        self.scroll_limit: int = scroll_limit

    def attach_chrome_driver(self) -> "SeleniumCrawler":
        self.set_driver("chrome").load_config()
        return self

    def attach_edge_driver(self) -> "SeleniumCrawler":
        self.set_driver("edge").load_config()
        return self

    def attach_firefox_driver(self) -> "SeleniumCrawler":
        self.set_driver("firefox").load_config()
        return self

    def build(self) -> "SeleniumCrawler":
        self._build()
        return self

    def get_driver(self):
        return self._driver
