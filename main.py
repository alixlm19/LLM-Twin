from llm_twin.crawlers.linkedin import LinkedInCrawler


def main():
    print("Hello from llm-twin!")

    crawler = LinkedInCrawler().attach_chrome_driver().build()
    crawler.driver.close()


if __name__ == "__main__":
    main()
