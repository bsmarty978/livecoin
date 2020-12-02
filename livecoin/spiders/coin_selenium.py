import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which


class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['www.livecoin.net']
    start_urls = [
        'https://www.livecoin.net/en'
    ]
    
    def __init__(self):
        chrome_opt = Options()
        chrome_opt.add_argument("--headless")
        driver_path = which("chromedriver")
        driver = webdriver.Chrome(executable_path=driver_path,options=chrome_opt)
        driver.set_window_size(1920,1080)

        driver.get("https://www.livecoin.net/en")

        tabs = driver.find_elements_by_class_name("filterPanelItem___2z5Gb")
        tabs[0].click()

        self.html  = driver.page_source

        driver.close()


    def parse(self, response):
        resp = Selector(text=self.html)
        for coin in resp.xpath("//div[contains(@class,'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield{
                'pair' : coin.xpath(".//div[1]/div/text()").get(),
                'volume' : coin.xpath(".//div[2]/span/text()").get()
            }
