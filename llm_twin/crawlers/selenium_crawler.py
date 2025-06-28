import time

from .base import SUPPORTED_DRIVER_TYPES, BaseSeleniumCrawler


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

    def set_extra_driver_options(self) -> None:
        pass

    def build(self) -> "SeleniumCrawler":
        self.set_extra_driver_options()
        self._build()
        return self

    @property
    def driver(self) -> SUPPORTED_DRIVER_TYPES:
        return self._driver

    def scroll_to_position(self, start: int, end: int) -> None:
        self.driver.execute_script(f"window.scrollTo({start}, {end});")

    def get_page_height(self) -> int:
        return self.driver.execute_script("return document.body.scrollHeight;")

    def scroll_page(self, wait_time: int = 5) -> None:
        """"""
        last_height: int = self.get_page_height()

        for _ in range(self.scroll_limit):
            self.scroll_to_position(0, last_height)
            time.sleep(wait_time)
            new_height: int = self.get_page_height()

            if last_height == new_height:
                break

            last_height = new_height
