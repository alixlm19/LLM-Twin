from llm_twin.crawlers.selenium_crawler import SeleniumCrawler
from llm_twin.domain.documents import PostDocument


class LinkedInCrawler(SeleniumCrawler):
    model = PostDocument

    def __init__(self, scroll_limit: int = 5, is_deprecated: bool = True) -> None:
        super().__init__(scroll_limit)
        self._is_deprecated = is_deprecated
