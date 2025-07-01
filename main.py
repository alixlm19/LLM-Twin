from loguru import logger

from llm_twin.crawlers.linkedin import LinkedInCrawler


def main():
    print("Hello from llm-twin!")

    crawler = LinkedInCrawler()
    try:
        crawler = crawler.attach_chrome_driver().build()
        crawler.login()
    except Exception as e:
        logger.error(f"Application crashed: {e}")
    finally:
        crawler.driver.close()


if __name__ == "__main__":
    main()
