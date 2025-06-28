from loguru import logger

from llm_twin.crawlers.selenium_crawler import SeleniumCrawler
from llm_twin.domain.documents import PostDocument
from llm_twin.settings import settings


class LinkedInCrawler(SeleniumCrawler):
    model = PostDocument

    def __init__(self, scroll_limit: int = 5, is_deprecated: bool = True) -> None:
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

    def login(self) -> None:
        if self._is_deprecated:
            raise DeprecationWarning(
                "As LinkedIn has updated its security measures, the login() mehot is no longer supported"
            )

        self.driver.get("https://www.linkedin.com/login")
        if not settings.LINKEDIN_USERNAME or not settings.LINKEDIN_PASSWORD:
            raise
