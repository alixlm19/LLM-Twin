from bs4 import BeautifulSoup
from loguru import logger

from llm_twin.crawlers.selenium_crawler import SeleniumCrawler
from llm_twin.domain.documents import ArticleDocument, UserDocument


class MediumCrawler(SeleniumCrawler[ArticleDocument]):
    model = ArticleDocument

    def set_extra_driver_option(self) -> None:
        self._options.add_argument(r"--profile-directory=Profile 2")

    def extract(self, url: str, /, **kwargs) -> None:
        """"""
        old_model = self.model.find(url=url)

        if old_model:
            logger.info(f"Article already exists in the database: {url}")
            return

        logger.info(f"Starting scraping Medium article: {url}")

        self.driver.get(url)
        self.scroll_page()

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        title = soup.find_all("h1", class_="pw-subtitle-paragraph")
        subtitle = soup.find_all("h2", class_="pw-subtitle-paragraph")

        data: dict[str, str | None] = {
            "Title": title[0].get_text(),
            "Subtitle": subtitle[0].get_text(),
            "Content": soup.get_text(),
        }

        self.driver.close()

        user: UserDocument = kwargs["user"]
        instance = self.model.model_construct(
            platform="Medium",
            content=data,
            url=url,
            author_id=user.id,
            author_full_name=user.full_name,
        )
        instance.save()

        logger.info(f"Successfully scraped and saved article: {url}")
