import time
from functools import lru_cache
from typing import Any, cast, override

from bs4 import BeautifulSoup
from loguru import logger
from selenium.webdriver.common.by import By

from llm_twin.crawlers.selenium_crawler import SeleniumCrawler
from llm_twin.decorators import check_if_deprecated
from llm_twin.domain.documents import PostDocument
from llm_twin.domain.exceptions import ImproperlyConfigured
from llm_twin.settings import settings


class LinkedInCrawler(SeleniumCrawler[PostDocument]):
    model = PostDocument

    def __init__(
        self,
        scroll_limit: int = 5,
        is_deprecated: bool = False,
        config_filename: str = "linkedin_crawler_config.toml",
    ) -> None:
        super().__init__(scroll_limit, config_filename)
        self._is_deprecated = is_deprecated
        self._last_url_scraped = ""

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
        logger.info("Attempting to log in.")
        self.driver.get("https://www.linkedin.com/login")
        if not settings.LINKEDIN_USERNAME or not settings.LINKEDIN_PASSWORD:
            raise ImproperlyConfigured(
                "LinkedIn scraper required the {LINKEDIN_USERNAME} and {LINKEDIN_PASSWORD} settings."
            )

        try:
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
        except Exception as e:
            logger.error(e)

    @override
    @logger.catch
    # @check_if_deprecated("This method is no longer supported")
    def extract(self, url: str, /, **kwargs) -> None:
        url = url.removesuffix("/")

        old_model = self.model.find(url=url)

        if old_model:
            logger.info(f"Article profile exists in the database: {url}")
            return

        logger.info(f"Starting scraping data for profile {url}")

        self.login()
        soup = self._get_page_content(url)
        data = {
            section: self._scrape_section(
                url=f"{url}/{config.get('path', '')}",
                attrs=config.get("attributes", dict()),
                **cast(dict[str, Any], config.get("kwargs")),
            )
            for section, config in self.crawler_config.items()
        }
        __import__("pprint").pprint(data)

    def _scrape_section(self, url: str, *args: Any, **kwargs: Any) -> str:
        """Scrape a specific section of the LinkedIn profile."""
        soup = self._get_page_content(url)
        parent_div = soup.find(*args, **kwargs)
        if parent_div:
            return parent_div.get_text(strip=True)

        return ""

    def _scrape_experience(self, profile_url: str) -> str:
        soup = self._get_page_content(profile_url + "/details/experience/")
        content = soup.find("section", {"id": "experience"})

        if content:
            return content.get_text(strip=True)

        return ""

    def _scrape_education(self, profile_url: str) -> str:
        pass

    @property
    def _soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.driver.page_source, "html.parser")

    @lru_cache
    def _get_page_content(self, url: str) -> BeautifulSoup:
        """Retrieve the page content of a given URL."""
        self.driver.get(url)
        time.sleep(5)

        return self._soup
