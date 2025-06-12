from selenium import webdriver

from .base import BaseSeleniumCrawler


class SeleniumCrawler(BaseSeleniumCrawler):
    def __init__(self, scroll_limit: int = 5) -> None:
        super().__init__()

        options: BaseSeleniumCrawler._DriverOptionsType = webdriver.ChromeOptions()
        self.set_extra_driver_options(options)

        self.scroll_limit: int = scroll_limit
        self.driver: _DriverType = webdriver.Chrome(options=options)

    @classmethod
    def build(cls) -> "SeleniumCrawler":
        crawler = cls()
        return crawler

    def attach_chrome_driver(self) -> "SeleniumCrawler":
        options: list[str] = [
            "--no-sandbox",
            "--headless=new",
            "--disable-dev-shm-usage",
            "--log-level=3",
            "--disable-popup-blocking",
            "--disable-notifications",
            "--disable-extensions",
            "--disable-background-networking",
            "--ignore-certificate-errors",
            "--user-data-dir={mkdtemp()}",
            "--data-path={mkdtemp()}",
            "--disk-cache-dir={mkdtemp()}",
            "--remote-debugging-port=9226",
        ]
        self.set_options(options, webdriver.ChromeOptions)

        return self
