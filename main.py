from selenium import webdriver

from llm_twin.crawlers.base import BaseSeleniumCrawler


def main():
    print("Hello from llm-twin!")
    b = BaseSeleniumCrawler()
    b.from_config()
    p = b.install_or_get_driver("chrome", install_if_missing=True)
    print(p)
    s = webdriver.ChromeService(p)
    webdriver.Chrome(options=b.options_handler, service=s)


if __name__ == "__main__":
    main()
