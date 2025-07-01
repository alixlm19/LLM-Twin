from typing import override

from loguru import logger
from selenium.webdriver.common.by import By

from llm_twin.crawlers.selenium_crawler import SeleniumCrawler
from llm_twin.decorators import check_if_deprecated
from llm_twin.domain.documents import PostDocument
from llm_twin.domain.exceptions import ImproperlyConfigured
from llm_twin.settings import settings


class LinkedInCrawler(SeleniumCrawler[PostDocument]):
    model = PostDocument

    def __init__(self, scroll_limit: int = 5, is_deprecated: bool = False) -> None:
        super().__init__(scroll_limit)
        self._is_deprecated = is_deprecated

    def set_extra_driver_options(self) -> None:
        if not self._options:
            logger.error("Driver Options not initialized.")
        logger.info(f"Adding extra options to {__class__}")
        func = getattr(
            self._options, "add_experimental_option", self._add_experimental_option
        )
        func("detach", True)

    @check_if_deprecated()
    def login(self) -> None:
        self.driver.get("https://www.linkedin.com/login")
        if not settings.LINKEDIN_USERNAME or not settings.LINKEDIN_PASSWORD:
            raise ImproperlyConfigured(
                "LinkedIn scraper required the {LINKEDIN_USERNAME} and {LINKEDIN_PASSWORD} settings."
            )

        self.driver.find_element(By.ID, "username").send_keys(
            settings.LINKEDIN_USERNAME
        )
        self.driver.find_element(By.ID, "password").send_keys(
            settings.LINKEDIN_PASSWORD
        )
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#organic-div > form > div.login__form_action_container > button",
        ).click()

    @override
    @check_if_deprecated("This method is no longer supported")
    def extract(self, url: str, /, **kwargs) -> None:
        if self.model.url:
            pass
