from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from preprocessor.data_loader import DataLoader
import regex as re

class ShopScraper():
    def __init__(self, formal_page=None):
        self.absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'
        self.initial_url = 'https://search.shopping.naver.com/mall/mall.nhn'
        self.partial_url = 'https://search.shopping.naver.com/search/all?'

        if formal_page != None :
            self.current_page = formal_page

        else :
            self.current_page = 1

        self.end_page = 2450

        self.data_set = []

    def set_initial_options(self, driver):
        category_filter_button = driver.find_element_by_xpath('//input[contains(@id, "cat_50000000")]')
        category_filter_button.click()

        # Try-Except because of Attach Error
        try :
            store_filter_button = driver.find_element_by_xpath('//input[contains(@id, "gift_shopn")]')
            store_filter_button.click()

        except :
            store_filter_button = driver.find_element_by_xpath('//input[contains(@id, "gift_shopn")]')
            store_filter_button.click()

        # Try-Except because of Attach Error 2
        try :
            product_filter_button = driver.find_element_by_xpath('//a[contains(@class, "_btn_count")]')
            product_filter_button.click()

        except :
            product_filter_button = driver.find_element_by_xpath('//a[contains(@class, "_btn_count")]')
            product_filter_button.click()

    def click_next_page(self, driver):
        next_page_button = driver.find_element_by_xpath('//a[contains(@onclick, "mall.changePage(' + str(self.current_page + 1) + ',")]')
        next_page_button.click()

        self.current_page += 1

    def mouse_over_on_tag(self, table_row, driver):
        action = ActionChains(driver)
        firstLevelMenu = table_row.find_element_by_xpath(xpath='descendant::td[contains(@class, "mall")]/a')
        action.move_to_element(firstLevelMenu).perform()

        url = driver.find_element_by_xpath(xpath='/html/body/div[2]/div[7]/div[1]/div/ul/li[2]/a').get_attribute('href')

        return url

    def main_process(self):
        # Start & Initialize Page
        driver = webdriver.Chrome(self.absolute_path + 'driver/chromedriver')#, options=options)
        driver.get(self.initial_url)

        self.set_initial_options(driver=driver)
        try :
            full_count = driver.find_element_by_xpath(xpath='/html/body/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/em').text
        except :
            full_count = driver.find_element_by_xpath(xpath='/html/body/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/em').text

        full_count = re.sub(pattern=',|개', repl='', string=full_count)

        # Click & Get Page
        while self.current_page <= self.end_page :
            time.sleep(1)

            # Get Table Tags
            table_tag = driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr')

            for idx, table_row in enumerate(table_tag):
                if idx == 0:
                    continue

                else :
                    mall_name = table_row.find_element_by_xpath(xpath='descendant::td[contains(@class, "mall")]/a[2]').text
                    mall_url = table_row.find_element_by_xpath(xpath='descendant::td[contains(@class, "url")]/p/a').text
                    mall_item_count = table_row.find_element_by_xpath(xpath='descendant::td[contains(@class, "item")]/strong/a').text
                    mall_item_detail_url = self.mouse_over_on_tag(table_row=table_row, driver=driver)

                    print(mall_name)
                    print(mall_url)
                    print(mall_item_count)
                    print(mall_item_detail_url)

                    print('-' * 50)
                    print(str(float(len(self.data_set) / float(full_count) * 100)) + '%')
                    print('-' * 50)

                    data = {'name':mall_name, 'url':mall_url, 'item_count':mall_item_count, 'detail_url':mall_item_detail_url}
                    self.data_set.append(data)

            # Click Next Button
            self.click_next_page(driver=driver)

        #
        driver.close()

        return self.data_set

if __name__ == "__main__" :
    shop_scraper = ShopScraper()
    data_set = shop_scraper.main_process()



    DataLoader().save_pickle_data(data=data_set, filepath='../database/shop/shop_FashionCloth_ver_1')
