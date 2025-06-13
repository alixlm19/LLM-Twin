import tomllib

from selenium import webdriver

from .base import BaseSeleniumCrawler, _DriverOptionsType


class SeleniumCrawler(BaseSeleniumCrawler):
    def __init__(self, scroll_limit: int = 5) -> None:
        super().__init__()

        options: _DriverOptionsType = webdriver.ChromeOptions()

        self.scroll_limit: int = scroll_limit
        self.driver: _DriverType = webdriver.Chrome(options=options)

    @classmethod
    def build(cls) -> "SeleniumCrawler":
        crawler = cls()
        return crawler

    def _read_config(
        self, path: str = "./configs/driver-settings.toml"
    ) -> _DriverOptionsType:
        with open(path, "rb") as f:
            config = tomllib.load(f)

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
