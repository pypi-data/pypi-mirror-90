from adnar_scraper import settings
import time
import regex as re

from multiprocessing import Process, Manager

from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper.utility.error_file_controller import ErrorFileController
from adnar_scraper.utility.selenium_controller import SeleniumController
from adnar_scraper.utility.save_file_controller import SaveFileController
from adnar_scraper.utility.database_controller import DatabaseController
from adnar_scraper.settings import SEO_DATABASE_PATH


class InfoDetailAttrUrlScraper:
    def __init__(self, filter_by_manual_list=None):
        '''
         Attribute Tagging 조합 scraper
        '''
        self.scraper_name = "info_detail_attr_url_scraper"
        self.kind = "item"

        self.selenium_controller = SeleniumController()
        self.starting_time = DataLoader.create_file_name()
        self.save_file_controller = SaveFileController(name=self.scraper_name, date_time=self.starting_time, kind=self.kind)
        self.error_file_controller = ErrorFileController(name=self.scraper_name, date_time=self.starting_time)
        self.database_controller = DatabaseController(selected_database=self.kind)

        if filter_by_manual_list is None:
            self.data_set = self.filter_gathered_data_set(category_data_set=DataLoader.load_data_from_csv_multi_with_encode(file_path=SEO_DATABASE_PATH + 'all_category_with_attr_url.csv', encoding='utf8'),
                                                          data_from_processes=self.database_controller.get_category_datas_in_path(db_name=self.scraper_name, process_num_list=[1, 2]))

        else:
            self.data_set = self.filter_by_manual(category_data_set=DataLoader.load_data_from_csv_multi_with_encode(file_path=SEO_DATABASE_PATH + 'all_category_with_attr_url.csv', encoding='utf8'),
                                                  manual_filter_list=filter_by_manual_list)

            for a in self.data_set:
                print(a)


        print('Category count: ' + str(len(self.data_set)))

        self.full_item_length = 0

    @staticmethod
    def reorganize_url(category_data):
        if len(category_data[-1]) != 0:
            front_url = "https://search.shopping.naver.com/search/category?catId=" + category_data[-3]
            max_price_url = "&frm=NVSHPRC&maxPrice="
            min_price_url = "&minPrice="
            paging_url = "&origQuery&pagingIndex="
            spec_url = "&pagingSize=40&productSet=total&query&sort=rel&spec="
            # None 경우 따져보자
            back_url = "&timestamp=&viewType=list"

            return {"front_url": front_url, "max_price_url": max_price_url, "min_price_url": min_price_url,
                    "paging_url": paging_url, "spec_url": spec_url, "back_url": back_url}

        else:
            front_url = "https://search.shopping.naver.com/search/category?catId=" + category_data[-3]
            max_price_url = "&frm=NVSHPRC&maxPrice="
            min_price_url = "&minPrice="
            paging_url = "&origQuery&pagingIndex="
            back_url = "&pagingSize=40&productSet=total&query&sort=rel&timestamp=&viewType=list"

            return {"front_url": front_url, "max_price_url": max_price_url, "min_price_url": min_price_url,
                    "paging_url": paging_url, "back_url": back_url}

    def multi_get_data(self, num_of_process):
        with Manager() as manager:
            data_len_list = manager.list()

            if num_of_process == 2:
                basis = len(self.data_set) // 2

                process_1 = Process(target=self.get_data, args=(0, basis * 1, data_len_list, 1))
                process_2 = Process(target=self.get_data, args=(basis * 1, len(self.data_set), data_len_list, 2))

                process_1.start()
                process_2.start()

                process_1.join()
                process_2.join()

            elif num_of_process == 4:
                basis = len(self.data_set) // 4

                process_1 = Process(target=self.get_data, args=(0, basis * 1, data_len_list, 1))
                process_2 = Process(target=self.get_data, args=(basis * 1, basis * 2, data_len_list, 2))
                process_3 = Process(target=self.get_data, args=(basis * 2, basis * 3, data_len_list, 3))
                process_4 = Process(target=self.get_data, args=(basis * 3, len(self.data_set), data_len_list, 4))

                process_1.start()
                process_2.start()
                process_3.start()
                process_4.start()

                process_1.join()
                process_2.join()
                process_3.join()
                process_4.join()

    @staticmethod
    def choose_price_step_period(full_num):
        if full_num < 8000:
            return {"price_step": 10000, "period": "range"}

        elif 8000 < full_num < 16000:
            return {"price_step": 1000, "period": "range"}

        else:
            return {"price_step": 500, "period": "range"}

    def get_data(self, start_index, end_index, data_len_list, process_num):
        print('Initiate Get data')
        self.error_file_controller.init_error_file(process_num=process_num)

        full_data_length = len(self.data_set[start_index:end_index])

        for d_idx, data_dict in enumerate(self.data_set[start_index:end_index]):
            data = data_dict["category_info"]
            formal_price = data_dict.get("formal_price")

            saving_list = []
            error_list = []

            #driver = self.selenium_controller.get_ghost_driver()
            driver = self.selenium_controller.get_image_blocked_driver(show_browser=False)
            #driver = self.selenium_controller.get_visual_driver()

            url_form = self.reorganize_url(category_data=data)

            if formal_price is None:
                initial_min_price = 1
            else:
                initial_min_price = formal_price

            initial_max_price = 100000
            '''
            {"front_url": front_url, "max_price_url": max_price_url, "min_price_url": min_price_url,
                "paging_url": paging_url, "spec_url": spec_url, "back_url": back_url}
            '''
            if len(data[-1]) != 0:
                initial_url = url_form["front_url"] + url_form["max_price_url"] + str(initial_max_price) + \
                              url_form["min_price_url"] + str(initial_min_price) + url_form["paging_url"] + str(1) + \
                              url_form["spec_url"] + data[-1] + url_form["back_url"]
            else:
                initial_url = url_form["front_url"] + url_form["max_price_url"] + str(initial_max_price) + \
                              url_form["min_price_url"] + str(initial_min_price) + url_form["paging_url"] + str(1) + \
                              url_form["back_url"]

            print(initial_url)

            full_num = self.selenium_controller.get_page_item_num(driver=driver, initial_url=initial_url)
            print("Process {} Full Item Num : {}".format(process_num, full_num))

            protocol = self.choose_price_step_period(full_num=full_num)
            print("Process {} protocol : {}".format(process_num, protocol))

            price = initial_min_price

            while price <= initial_max_price:
                #나중에 1 없애야함
                min_price = None
                max_price = None

                if protocol["period"] == "range":
                    if price != 1:
                        price = price // 100 * 100

                    min_price = price
                    max_price = price + protocol["price_step"]
                    price = max_price

                elif protocol["period"] == "same":
                    if price != 1:
                        price = price // 100 * 100

                    min_price = price
                    max_price = price
                    price += protocol["price_step"]

                print("Process {} MinPrice : {}, MaxPrice : {}, SavingListLength : {}".format(process_num, min_price, max_price - 1, (len(saving_list))))

                if len(data[-1]) != 0:
                    count_purpose_url = url_form["front_url"] + url_form["max_price_url"] + str(max_price - 1) + \
                                        url_form["min_price_url"] + str(min_price) + url_form["paging_url"] + str(1) + \
                                        url_form["spec_url"] + data[-1] + url_form["back_url"]
                else:
                    count_purpose_url = url_form["front_url"] + url_form["max_price_url"] + str(max_price - 1) + \
                                        url_form["min_price_url"] + str(min_price) + url_form["paging_url"] + str(1) + \
                                        url_form["back_url"]

                full_page = self.get_full_page(
                    item_count=self.selenium_controller.get_page_item_num(driver=driver, initial_url=count_purpose_url))

                if full_page == 0:
                    print("CONTINUE")
                    continue

                else:
                    for page_num in range(full_page):
                        page_num += 1

                        if len(data[-1]) != 0:
                            url = url_form["front_url"] + url_form["max_price_url"] + str(max_price - 1) + \
                                  url_form["min_price_url"] + str(min_price) + url_form["paging_url"] + str(page_num) + \
                                  url_form["spec_url"] + data[-1] + url_form["back_url"]
                        else:
                            url = url_form["front_url"] + url_form["max_price_url"] + str(max_price - 1) + \
                                  url_form["min_price_url"] + str(min_price) + url_form["paging_url"] + str(page_num) + \
                                  url_form["back_url"]

                        driver.get(url=url)

                        extracted_data = self.get_info_data(driver=driver)

                        if len(extracted_data['extracted_list']) == 0 or page_num > 200:
                            break

                        if len(saving_list) + len(extracted_data['extracted_list']) < 5000 or page_num == full_page:
                            saving_list += extracted_data['extracted_list']

                        else:
                            data_len_list.append(len(saving_list))
                            print('-'*50)
                            print(f"Saving {data[0:3]}, Process {process_num}, Price {min_price}~{max_price}")
                            self.save_file_controller.save_data_memory_saving_version(process_num=process_num,
                                                                                      data_set=saving_list)
                            saving_list = []
                            saving_list += extracted_data['extracted_list']

                        error_list += extracted_data['error_list']
                        self.error_file_controller.save_error(process_num=process_num, errors=error_list)

            if d_idx + 1 == full_data_length and len(saving_list) != 0:
                self.save_file_controller.save_data_memory_saving_version(process_num=process_num,
                                                                          data_set=saving_list)

            print('-' * 100)
            print("Process {}- Current Percent : {}, Current saved data : {}".format(process_num, (d_idx / full_data_length * 100), sum(data_len_list)))
            print('-' * 100)
            driver.close()

    def get_info_data(self, driver):
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
                        "category_name": category_name}

            if data_set['image_link'] != None:
                extracted_list.append(data_set)

        return {"extracted_list": extracted_list, "error_list": error_list}

    @staticmethod
    def get_full_page(item_count):
        if item_count is None:
            full_page = 0

        else:
            item_count = int(item_count)
            full_page = item_count // 40 + 1

            if full_page > 200:
                full_page = 199

        return full_page

    @staticmethod
    def get_category_key(data):
        try:
            return str(data["main_category"] + data["sub_category"] + data["category_name"])

        except:
            return str(data[0] + data[1] + data[2])

    @staticmethod
    def filter_by_manual(manual_filter_list, category_data_set):
        none_gathered_category = []

        for category_data in category_data_set:
            for manual_data in manual_filter_list:
                if category_data[:3] == manual_data[:3]:
                    if len(manual_data) == 4:
                        none_gathered_category.append({"category_info":category_data, "formal_price": manual_data[3]})

                    else:
                        none_gathered_category.append({"category_info": category_data})

        return none_gathered_category

    def filter_gathered_data_set(self, category_data_set, data_from_processes):
        none_gathered_category = []
        process_categories = {}

        for data_from_process_dict in data_from_processes:
            process_num = data_from_process_dict['process_num']
            data_from_process = data_from_process_dict['item_list']

            if len(data_from_process) != 0:
                last_process_category = "Currently Stopped"#self.get_category_key(data=data_from_process[-1])

                for item in data_from_process:
                    item_key = self.get_category_key(item)

                    if item_key in process_categories:
                        continue

                    elif item_key not in process_categories and item_key != last_process_category:
                        process_categories[item_key] = 1

        for category in category_data_set:
            category_key = self.get_category_key(data=category)

            if category_key not in process_categories:
                none_gathered_category.append(category)

        for c in process_categories.keys():
            print('Already gathered! : {}'.format(c))

        return none_gathered_category

if __name__ == "__main__":
    '''
    1. gathered dataset 
    2. os specific scraping
    '''
    '''
    이 부분을 하면 된다!!!!!!!!!!!!! 일어나서 이거 내 컴퓨터로 옮기고 하자
    
    '''
    scraper = InfoDetailAttrUrlScraper(filter_by_manual_list=[['패션의류', '여성의류', '조끼'], ['패션의류', '여성의류', '정장세트'], ['패션의류', '여성의류', '한복'], ['패션의류', '여성의류', '파티복']])
    scraper.multi_get_data(num_of_process=2)

    #https://search.shopping.naver.com/search/category?catId=50000805&frm=NVSHPRC&maxPrice=9&minPrice=1&origQuery&pagingIndex=1&pagingSize=40&productSet=total&query&sort=price_asc&spec=M10013498%7CM10557683%20M10013498%7CM10904496%20M10013498%7CM10557685&timestamp=&viewType=list
    #https://search.shopping.naver.com/search/category?catId=50000805&frm=NVSHPRC&maxPrice=9&minPrice=1&origQuery&pagingIndex=1&pagingSize=40&productSet=total&query&sort=price_asc&spec=M10013498%7CM10557683%20M10013498%7CM10904496%20M10013498%7CM10557685&timestamp=&viewType=list