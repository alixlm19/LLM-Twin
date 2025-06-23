from llm_twin.crawlers.selenium_crawler import SeleniumCrawler


def main():
    print("Hello from llm-twin!")
<<<<<<< Updated upstream
    # b = BaseSeleniumCrawler()
    # b.from_config()
    # p = b._install_or_get_driver("chrome", install_if_missing=True)
    # print(p)
    # s = webdriver.ChromeService(p)
    # driver = webdriver.Chrome(options=b.options_handler, service=s)

    crawler = SeleniumCrawler().attach_chrome_driver().build()
    driver = crawler.get_driver()
    driver.get("https://www.google.com")
    print(driver.page_source)
=======
    b = BaseSeleniumCrawler()
    b.from_config()
    p = b.install_or_get_driver("edge", install_if_missing=True)
    print(p)
    s = webdriver.EdgeService(executable_path=p)

    d = webdriver.Edge(options=b.options_handler, service=s)
    d.get("https://www.google.com")
    print(d.page_source)
>>>>>>> Stashed changes


if __name__ == "__main__":
    main()
