import re
import time
from functools import lru_cache
from typing import Any, Iterable, cast, override

from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement
from loguru import logger
from selenium.webdriver.common.by import By

from llm_twin.crawlers.exceptions import UnsupportedTagError
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

        self.driver.find_element(By.ID, "username").send_keys(
            settings.LINKEDIN_USERNAME
        )
        self.driver.find_element(By.ID, "password").send_keys(
            settings.LINKEDIN_PASSWORD
        )
        self.driver.find_element(
            By.XPATH, "//*[@id='organic-div']/form/div[4]/button"
        ).click()
        logger.success("Logged in!")

    @override
    @logger.catch
    @check_if_deprecated("This method is no longer supported")
    def extract(self, url: str, /, **kwargs) -> None:
        url = url.removesuffix("/")

        old_model = self.model.find(url=url)

        if old_model:
            logger.info(f"LinkedIn post already exists in the database: {url}")
            return

        logger.info(f"Starting scraping data for profile {url}")

        self.login()
        data: dict[str, str | list[str]] = dict()
        children: dict[str, str] = dict()

        for section, values in self.crawler_config.items():
            section_url: str = f"{url}/{values.get('path', '')}"
            section_tag: str = values["tag"]
            section_attrs: dict[str, Any] = values.get("attrs", dict())
            section_kwargs: dict[str, Any] = values.get("kwargs", dict())
            section_children: dict[str, Any] | None = values.get("children")

            if section_kwargs.get("class_"):
                section_kwargs["class_"] = re.compile(section_kwargs.get("class_", ""))

            if section_children:
                for child, child_dict in section_children.items():
                    data[f"{section}-{child}"] = self._scrape_section(
                        url=section_url,
                        tag=section_tag,
                        children=child_dict,
                        attrs=section_attrs,
                        **section_kwargs,
                    )
            else:
                data[section] = self._scrape_section(
                    url=section_url,
                    tag=section_tag,
                    attrs=section_attrs,
                    **section_kwargs,
                )

        for k, v in data.items():
            print(k, end=": ")
            if isinstance(v, list):
                for vv in v:
                    print(v)
                    print("*" * 80)
                    print()
            else:
                print(v)
        # data = {
        #     section: self._scrape_section(
        #         url=f"{url}/{config.get('path', '')}",
        #         attrs=config.get("attributes", dict()),
        #         **cast(dict[str, Any], config.get("kwargs", dict())),
        #     )
        #     for section, config in self.crawler_config.items()
        # }
        return

        self.driver.get(url)
        time.sleep(5)
        button = self.driver.find_element()
        button.click()

        self.scroll_page()
        soup = self._soup

    def _scrape_section(
        self,
        url: str,
        tag: str,
        *args: Any,
        children: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> str | list[str]:
        """Scrape a specific section of the LinkedIn profile."""

        result: str | list[str]
        element: PageElement | Tag | None = None
        element_children: Iterable[PageElement] | Iterable[Tag] = []
        children_tag: str = ""

        soup = self._get_page_content(url)
        element = soup.find(tag, *args, **kwargs)

        if children:
            children_tag: str = children.get("tag", "")
            children_attrs: dict[str, Any] = children.get("attrs", dict())
            children_kwargs: dict[str, Any] = children.get("kwargs", dict())
            if children_kwargs.get("class_"):
                children_kwargs["class_"] = re.compile(
                    children_kwargs.get("class_", "")
                )

            element_children = cast(Tag, element).find_all(
                children_tag, children_attrs, **children_kwargs
            )

        if not element and not element_children:
            return ""

        target_tag = tag if not element_children else children_tag
        target_element = element if not element_children else element_children

        match target_tag:
            case "div" | "h1" | "main":
                div: PageElement = cast(PageElement, target_element)
                result = div.get_text(strip=True)
            case "img":
                img: Tag = cast(Tag, target_element)
                if img.has_attr("img"):
                    result = cast(str, img["src"])
            case "li":
                result = []

                for li in cast(Iterable, target_element):
                    result.append("".join(li.get_text(strip=True)))
            case _:
                raise UnsupportedTagError(f"Cannot crawl the specified tag: {tag}")

        return result

    @property
    def _soup(self) -> BeautifulSoup:
        logger.info(f"Generating soup for url: {self.driver.current_url}")
        return BeautifulSoup(self.driver.page_source, "html.parser")

    @lru_cache
    def _get_page_content(self, url: str) -> BeautifulSoup:
        """Retrieve the page content of a given URL."""
        self.driver.get(url)
        time.sleep(5)

        return self._soup
