from selenium.webdriver.common.by import By
from config import DRIVER_PATH, URL
from selenium import webdriver
from db import find_all_search, process_merries


class ParserMerries():
    def __init__(self, url, bot=None):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.minimize_window()
        self.url = url
        self.bot = bot

    def __del__(self):
        self.driver.close()

    async def parse(self):
        search_models = find_all_search()
        for page in range(1, 3):
            print(self.url.format(page))
            self.driver.get(self.url.format(page))
            items = len(self.driver.find_elements(by=By.XPATH, value='//*[@class="product-card-list"]'))
            #items1 = len(self.driver.find_elements(by=By.XPATH, value='//*[@class="product-card j-card-item j-good-for-listing-event"]'))
            for item in range(items):
                merriess = self.driver.find_elements(by=By.XPATH, value='//*[@class="product-card j-card-item"]')
                for merrie in merriess:
                    #product_item = merrie.find_element(by=By.XPATH, value='//*[@class="brand-name"]')
                    product_href = merrie.find_element(by=By.XPATH, value='//*[@class="product-card__main j-card-link"]')
                    product_item = merrie.find_element(by=By.XPATH, value='//*[@class="goods-name"]')
                    #product_item = (f'{product_item0.text} / {product_item1.text}')
                    merries_title = product_item.text
                    merries_href = product_href.get_attribute('href')
                    for search_model in search_models:
                        if merries_title.find(search_model.title) >= 0:
                            await process_merries(merries_title, merries_href, search_model.chatid, self.bot)
