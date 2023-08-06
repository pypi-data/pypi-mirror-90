from adnar_scraper import settings
import time
import regex as re

from multiprocessing import Process, Manager

from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper.utility.error_file_controller import ErrorFileController
from adnar_scraper.utility.selenium_controller import SeleniumController
from adnar_scraper.utility.save_file_controller import SaveFileController
from adnar_scraper.utility.database_controller import DatabaseController


class ShopDetailScraper:
    def __init__(self, data_set):
        self.scraper_name = "shop_detail_scraper/ver_1"
        self.kind = "item"

        self.selenium_controller = SeleniumController()
        self.starting_time = DataLoader.create_file_name()
        self.save_file_controller = SaveFileController(name=self.scraper_name, date_time=self.starting_time, kind=self.kind)
        self.error_file_controller = ErrorFileController(name=self.scraper_name, date_time=self.starting_time)
        self.database_controller = DatabaseController(selected_database=self.kind)

        self.data_set = self.deleted_already_in_db(mall_db=data_set)

        print('Mall count: ' + str(len(self.data_set)))

        self.full_item_length = 100000

    def multi_get_data(self, num_of_process):
        with Manager() as manager:
            data_len_list = manager.list()

            if num_of_process == 2:
                basis = len(self.data_set) // 2

                process_1 = Process(target=self.get_data, args=(0, basis * 1, data_len_list, 1))
                process_2 = Process(target=self.get_data, args=(
                    basis * 1, basis * len(self.data_set), data_len_list, 2))

                process_1.start()
                process_2.start()

                process_1.join()
                process_2.join()

            elif num_of_process == 3:
                basis = len(self.data_set) // 3

                process_1 = Process(target=self.get_data, args=(0, basis * 1, data_len_list, 1))
                process_2 = Process(target=self.get_data,
                                    args=(basis * 1, basis * 2, data_len_list, 2))
                process_3 = Process(target=self.get_data,
                                    args=(
                                        basis * 2, basis * len(self.data_set), data_len_list, 3))

                process_1.start()
                process_2.start()
                process_3.start()

                process_1.join()
                process_2.join()
                process_3.join()

            elif num_of_process == 4:
                basis = len(self.data_set) // 4

                process_1 = Process(target=self.get_data, args=(0, basis * 1, data_len_list, 1))
                process_2 = Process(target=self.get_data,
                                    args=(basis * 1, basis * 2, data_len_list, 2))
                process_3 = Process(target=self.get_data,
                                    args=(basis * 2, basis * 3, data_len_list, 3))
                process_4 = Process(target=self.get_data,
                                    args=(
                                        basis * 3, basis * len(self.data_set), data_len_list, 4))

                process_1.start()
                process_2.start()
                process_3.start()
                process_4.start()

                process_1.join()
                process_2.join()
                process_3.join()
                process_4.join()

    def get_data(self, start_index, end_index, data_len_list, process_num):
        print('Initiate Get data')
        self.error_file_controller.init_error_file(process_num=process_num)

        for data in self.data_set[start_index:end_index]:
            saving_list = []
            error_list = []

            driver = self.selenium_controller.get_image_blocked_driver(show_browser=False)

            reorganized_url = self.reorganize_url(url=data['detail_url'])

            front_url = reorganized_url['front_url']
            back_url = reorganized_url['back_url']

            full_page = self.get_full_page(item_count=data['item_count'])

            for page_num in range(full_page):
                page_num += 1

                url = front_url + str(page_num) + back_url

                driver.get(url=url)

                extracted_data = self.get_info_data(driver=driver, mall_name=data['name'])
                saving_list += extracted_data['extracted_list']
                error_list += extracted_data['error_list']

            data_len_list.append(len(saving_list))
            self.save_file_controller.save_data_memory_saving_version(process_num=process_num, data_set=saving_list)
            self.error_file_controller.save_error(process_num=process_num, errors=error_list)

            self.selenium_controller.print_percent(full_item_length=self.full_item_length, data_len_list=data_len_list)

            driver.close()

    def get_info_data(self, driver, mall_name):
        error_list = []
        extracted_list = []

        # Scroll down to bottom
        self.selenium_controller.get_to_bottom(driver=driver, scroll_pause_time=0.3)

        template = driver.find_elements_by_xpath('//li[contains(@class, "basicList_item")]')

        for idx, element in enumerate(template):
            driver.execute_script("arguments[0].scrollIntoView();", element)
            # time.sleep(0.2)

            # Get Detail Info & If there is no detail then "Continue"
            temp_info_list = element.find_elements_by_xpath(
                xpath='descendant::a[contains(@class, "basicList_detail__")]')

            if len(temp_info_list) == 0:
                continue

            unfiltered_info_list = []

            for info in temp_info_list:
                info_text = re.sub(pattern=' ', repl='', string=info.text)

                if len(info_text) == 0:
                    pass

                elif re.search(pattern=':', string=info_text) != None:
                    unfiltered_info_list.append(info_text)

                else:
                    unfiltered_info_list[-1] = unfiltered_info_list[-1] + ',' + info_text

            filtered_info_list = []

            for info in unfiltered_info_list:
                splited_info = info.split(':')

                each_info = {splited_info[0]: splited_info[1].split(',')}
                filtered_info_list.append(each_info)

            # Get Name & Item URL
            item_basic_info = element.find_element_by_xpath(
                xpath='descendant::div[contains(@class, "basicList_title")]/a')

            item_name = item_basic_info.text
            item_url = item_basic_info.get_attribute('href')

            tag_data = self.selenium_controller.get_tag_in_new_tab(driver=driver, item_url=item_url)

            # Get Category
            main_category = None
            sub_category = None
            category_name = None

            try:
                category_basic_info = element.find_elements_by_xpath(xpath='descendant::div[contains(@class, "basicList_depth")]/a')
                main_category = category_basic_info[0].text
                sub_category = category_basic_info[1].text
                category_name = category_basic_info[2].text

            except Exception as e:
                print(e)

            # Get Item Price
            item_price = None

            try :
                item_price = element.find_element_by_xpath(
                    xpath='descendant::span[contains(@class, "price_num")]').text

            except Exception as e:
                print("Error message ! - In stage 1")
                print(e)
                error_list.append([e, "Inner"])

            # Get Image href
            image_link = None

            try:
                image_link = element.find_element_by_xpath(
                    xpath='descendant::a[contains(@class, "thumbnail_thumb")]/img').get_attribute('src')

            except Exception as e:
                print("Error message ! - In stage 1")
                print(e)
                error_list.append([e, "Inner"])
                time.sleep(0.3)

            # Set datas (Categories and data)
            data_set = {'item_name': item_name, 'info_list': filtered_info_list, 'image_link': image_link,
                        'tag_data': tag_data, 'item_price': item_price,
                        "main_category": main_category, "sub_category": sub_category,
                        "category_name": category_name, "mall_name": mall_name}

            if data_set['image_link'] != None:
                extracted_list.append(data_set)

        return {"extracted_list": extracted_list, "error_list": error_list}

    def get_full_page(self, item_count):
        full_page = 0

        item_count = re.sub(pattern='\,', repl='', string=item_count)
        item_count = int(item_count)

        if item_count <= 40:
            full_page = 1

        elif 40 < item_count <= 80:
            full_page = 2

        elif 80 < item_count:
            full_page = 3

        return full_page

    @staticmethod
    def reorganize_url(url):
        query = re.sub(pattern='https:\/\/search.shopping.naver.com\/search\/all\.nhn\?query\=|mall\=', repl='', string=url)
        query_list = query.split('&')

        filtered_query = query_list[0]
        mall_code = query_list[1]

        front_url = 'https://search.shopping.naver.com/search/all?mall=' + mall_code + '&origQuery=' + filtered_query + '&pagingIndex='
        back_url = '&pagingSize=40&productSet=total&query=' + filtered_query + '&sort=rel&timestamp=&viewType=list'

        return {'front_url':front_url, 'back_url':back_url}

    def deleted_already_in_db(self, mall_db):
        # Get all file in db
        mall_names = self.database_controller.get_mall_name_in_path(db_name=settings.ITEM_DATABASE_PATH + self.scraper_name + '/')

        # return filtered_data_set
        new_filtered_mall_list = []

        for each_mall in mall_db:
            is_in_data = False

            for mall in mall_names:
                if each_mall['name'] == mall:
                    is_in_data = True
                    break

            if is_in_data is False:
                new_filtered_mall_list.append(each_mall)

        return new_filtered_mall_list


if __name__ == "__main__":
    # x~100
    from adnar_scraper.utility.shop_analyzer import ShopAnalyzer
    from adnar_scraper.settings import LINUX_SHOP_DATABASE_PATH

    mall_infos = DataLoader.load_pickle_data(file_path=LINUX_SHOP_DATABASE_PATH + 'shop_FashionCloth_ver_1.pkl')

    shop_with_items = DatabaseController(selected_database='item').get_shop_count_data(db_name='shop_detail_scraper')
    shop_with_graphs = DatabaseController(selected_database='local_shop').get_recent_data(
        db_name='shop_follower_info_scraper')


    analyzer = ShopAnalyzer()

    filtered_mall = analyzer.get_shop_included_with_mall_data(shop_graph_data_set=shop_with_graphs,
                                                              show_item_data_set=shop_with_items,
                                                              mall_info_data_set=mall_infos)

    scraper = ShopDetailScraper(data_set=filtered_mall)
    scraper.multi_get_data(num_of_process=2)