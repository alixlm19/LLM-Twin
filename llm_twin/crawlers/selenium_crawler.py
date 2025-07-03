import os
import time
import tomllib
from functools import cached_property
from typing import Optional, Self

from loguru import logger

from llm_twin import settings

from .base import SUPPORTED_DRIVER_TYPES, BaseSeleniumCrawler


class SeleniumCrawler[DocT](BaseSeleniumCrawler[DocT]):
    def __init__(
        self, scroll_limit: int = 5, config_filename: Optional[str] = ""
    ) -> None:
        super().__init__()

        self.scroll_limit: int = scroll_limit
        self._crawler_config_filename: Optional[str] = config_filename

    def attach_chrome_driver(self) -> Self:
        self.set_driver("chrome").load_config()
        return self

    def attach_edge_driver(self) -> Self:
        self.set_driver("edge").load_config()
        return self

    def attach_firefox_driver(self) -> Self:
        self.set_driver("firefox").load_config()
        return self

    def set_extra_driver_options(self) -> None:
        pass

    def build(self) -> Self:
        self.set_extra_driver_options()
        self._build()
        return self

    @property
    def driver(self) -> SUPPORTED_DRIVER_TYPES:
        return self._driver

    @cached_property
    def crawler_config(
        self,
    ) -> dict[str, dict[str, str | dict[str, str]] | list[dict[str, str]]]:
        if not self._crawler_config_filename:
            raise FileNotFoundError("No config file was specified.")

        path_to_config = os.path.join(
            settings.DEFAULT_CRAWLER_CONFIG_PATH, self._crawler_config_filename
        )

        if not os.path.exists(path_to_config):
            raise FileNotFoundError(
                f"Could not find configuration file @ {path_to_config}."
            )

        with open(path_to_config, "rb") as f:
            config = tomllib.load(f)

        logger.info(f"Configuration file [{self._crawler_config_filename}] loaded.")

        return config

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
