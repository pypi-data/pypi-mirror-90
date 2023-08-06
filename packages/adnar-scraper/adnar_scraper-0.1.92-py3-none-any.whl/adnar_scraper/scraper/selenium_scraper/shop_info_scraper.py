from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper.utility.error_file_controller import ErrorFileController
from adnar_scraper.utility.selenium_controller import SeleniumController
from adnar_scraper.utility.save_file_controller import SaveFileController
from adnar_scraper.utility.database_controller import DatabaseController
from adnar_scraper.settings import SEO_DATABASE_PATH

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class ShopInfoScraper:
    def __init__(self, formal_page=None):
        self.scraper_name = "shop_info_scraper"
        self.kind = "local_shop"

        self.selenium_controller = SeleniumController()
        self.starting_time = DataLoader.create_file_name()
        self.save_file_controller = SaveFileController(name=self.scraper_name, date_time=self.starting_time,
                                                       kind=self.kind)
        self.database_controller = DatabaseController(selected_database=self.kind)

        # Load last save point if condition
        if formal_page is not None:
            self.current_page = formal_page

        else:
            self.current_page = 1

    def click_filter_fashion(self, driver):
        filter_btn_xpath = '//*[@id="cat_50000000"]'

        filter_btn = driver.find_element_by_xpath(xpath=filter_btn_xpath)
        filter_btn.click()

    def click_show_100_items(self, driver):
        filter_btn_xpath = '/html/body/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td/div/div[2]/div/div/p/a[3]'

        filter_btn = driver.find_element_by_xpath(xpath=filter_btn_xpath)
        filter_btn.click()

    def click_show_only_smart_stores(self, driver):
        filter_btn_xpath = '//*[@id="gift_shopn"]'

        filter_btn = driver.find_element_by_xpath(xpath=filter_btn_xpath)
        filter_btn.click()

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

    def get_shop_list_and_filter(self, num_of_shop=52115):
        # define list
        shop_data_list = []

        # Create driver, get web
        url = "https://search.shopping.naver.com/mall/mall.nhn"

        driver = self.selenium_controller.get_visual_driver()
        driver.get(url)

        # Click filter (Get only fashion mall, get each 100 shops per page)
        self.click_filter_fashion(driver=driver)
        self.click_show_only_smart_stores(driver=driver)

        # Get shop each page
        sleeping_time = 6

        full_page = num_of_shop // 20 + 1

        while self.current_page <= full_page:
            time.sleep(sleeping_time)

            # Get Shops
            for idx, each_shop_row in enumerate(driver.find_elements_by_xpath(xpath='//*[@id="mall_area"]/div[2]/table/tbody/tr')):
                if idx == 0:
                    continue

                shop_name = each_shop_row.find_element_by_xpath(xpath='descendant::td[1]/a[2]').text
                num_of_item = each_shop_row.find_element_by_xpath(xpath='descendant::td[4]/strong/a').text
                web_url = each_shop_row.find_element_by_xpath(xpath='descendant::td[2]/p/a').text
                web_detail_url = self.mouse_over_on_tag(table_row=each_shop_row, driver=driver)

                data_dict = {"name": shop_name, "num_of_item": num_of_item, "url": web_url, "detail_url": web_detail_url}
                shop_data_list.append(data_dict)

                print(f"Current Page : {self.current_page}")
                print(f'shop_name : {shop_name} \nitem_num: {num_of_item} \nweb_url: {web_url} \ndetail_url:{web_detail_url}')
                print("-"*50)

            self.click_next_page(driver=driver)

        self.save_file_controller.save_data_memory_with_out_process(data_set=shop_data_list)

if __name__ == "__main__":
    scraper = ShopInfoScraper()
    scraper.get_shop_list_and_filter()