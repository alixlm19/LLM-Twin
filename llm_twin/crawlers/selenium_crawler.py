from .base import BaseSeleniumCrawler


class SeleniumCrawler(BaseSeleniumCrawler):
    @classmethod
    def build(cls) -> "SeleniumCrawler":
        crawler = cls()
        return crawler
