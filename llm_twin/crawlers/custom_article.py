from urllib.parse import urlparse

from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers.html2text import Html2TextTransformer
from loguru import logger

from llm_twin.domain.documents import ArticleDocument, UserDocument

from .selenium_crawler import SeleniumCrawler


class CustomArticleCrawler(SeleniumCrawler):
    model = ArticleDocument

    def __init__(self) -> None:
        super().__init__()

    def extract(self, url: str, /, **kwargs) -> None:
        old_model = self.model.find(url=url)

        if old_model:
            logger.info(f"Article already exists in the database: {url}")
            return

        logger.info(f"Starting scraping article: {url}")

        loader = AsyncHtmlLoader([url])
        documents = loader.load()

        html2text = Html2TextTransformer()
        transformed_documents_collection = html2text.transform_documents(documents)
        tranformed_document = transformed_documents_collection[0]

        content: dict[str, str | None] = {
            "Title": tranformed_document.metadata.get("title"),
            "Subtitle": tranformed_document.metadata.get("description"),
            "Content": tranformed_document.page_content,
            "Language": tranformed_document.metadata.get("language"),
        }

        parsed_url = urlparse(url)
        platform = parsed_url.netloc

        user: UserDocument = kwargs["user"]
        instance = self.model.model_construct(
            content=content,
            url=url,
            platform=platform,
            author_id=user.id,
            author_full_name=user.full_name,
        )
        instance.save()

        logger.info(f"Finished scraping custom article: {url}")
