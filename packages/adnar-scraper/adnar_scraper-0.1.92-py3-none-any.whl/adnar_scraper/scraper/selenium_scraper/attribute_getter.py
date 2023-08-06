from adnar_scraper.settings import SEO_DATABASE_PATH
from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper.utility.error_file_controller import ErrorFileController
from adnar_scraper.utility.selenium_controller import SeleniumController
from adnar_scraper.utility.save_file_controller import SaveFileController
from adnar_scraper.utility.database_controller import DatabaseController
import time
import regex as re


class AttributeGetter:
    def __init__(self):
        self.scraper_name = 'attribute_getter'
        self.kind = 'seo_information'

        self.category_list = DataLoader.load_data_from_csv_multi_with_encode(file_path=SEO_DATABASE_PATH + 'all_category_with_attr.csv',
                                                                             encoding='utf8')

        self.base_url = {'front':'https://search.shopping.naver.com/search/category?catId=',
                         'back':'&origQuery&pagingIndex=1&pagingSize=40&productSet=total&query&sort=rel&timestamp=&viewType=list'}

        self.selenium_controller = SeleniumController()
        self.starting_time = DataLoader.create_file_name()
        self.save_file_controller = SaveFileController(name=self.scraper_name, date_time=self.starting_time,
                                                       kind=self.kind)
        self.error_file_controller = ErrorFileController(name=self.scraper_name, date_time=self.starting_time)
        self.database_controller = DatabaseController(selected_database=self.kind)

    def get_attributes(self):
        new_category_list = []

        for idx, category in enumerate(self.category_list):
            driver = self.selenium_controller.get_visual_driver(additional_option_list=None)

            reorganized_url = self.base_url['front'] + category[-2] + self.base_url['back']

            driver.get(reorganized_url)
            time.sleep(1.5)

            poll_elements = driver.find_elements_by_xpath(xpath='//div[contains(@class, "filter_finder_tit")]')

            selected_element = None

            if category[-1] != "None":
                for poll_idx, poll in enumerate(poll_elements):
                    if poll.text == category[-1]:
                        selected_element = poll.find_element_by_xpath('..')
                        break
                print(category)
                li_elements = selected_element.find_elements_by_xpath('descendant::ul[contains(@class, "filter_finder_list")]/li')

                for li_element in li_elements:
                    li_element.click()

                time.sleep(1.5)

                driver.refresh()

                current_url = driver.current_url

                filter_code = current_url.split('spec=')[-1].split('&timestamp')[0]
                print("filter code : {}".format(filter_code))

                new_category = category
                new_category.append(filter_code)

                new_category_list.append(new_category)

            else:
                new_category = category
                new_category.append(None)

                print("filter code : None")

                new_category_list.append(new_category)

            driver.close()
        return new_category_list


if __name__ == "__main__":
    getter = AttributeGetter()
    new_category_list = getter.get_attributes()

    DataLoader.write_data_in_csv_with_encode_multi(data_list=new_category_list, path=SEO_DATABASE_PATH + 'all_category_with_attr_url.csv', encoding='utf8')