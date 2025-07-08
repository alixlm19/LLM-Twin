from loguru import logger

from llm_twin import settings
from llm_twin.crawlers.linkedin import LinkedInCrawler


def main():
    print("Hello from llm-twin!")

    settings.LINKEDIN_USERNAME = "alixlm19@hotmail.com"
    settings.LINKEDIN_PASSWORD = "AU4L3-BdcpYd!SE"
    crawler = LinkedInCrawler()
    try:
        crawler = crawler.attach_chrome_driver().build()
        crawler.extract("https://www.linkedin.com/in/alixleon")
    except Exception as e:
        logger.error(f"Application crashed: {e}")
    finally:
        crawler.driver.close()


if __name__ == "__main__":
    main()
