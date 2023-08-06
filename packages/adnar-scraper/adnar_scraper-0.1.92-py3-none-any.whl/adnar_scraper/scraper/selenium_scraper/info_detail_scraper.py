import csv
from selenium import webdriver
import time
import regex as re
import hickle, pickle

from random import randint

from fake_useragent import UserAgent

import glob
import json

'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
'''
from multiprocessing import Process, Manager
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os

class MergeItems() :
    # Load, Merge, than delete formal data

    def __init__(self, item_folder_name=None):
        self.absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'
        self.last_folder_name = self.get_last_folder()
        self.item_folder_name = item_folder_name

    def get_last_folder(self):
        folder_list = glob(self.absolute_path + 'database/datas/' + "*/")

        time_with_folder = []

        for time_folder in folder_list:
            time_stamp = re.sub(pattern='/', repl=' ', string=time_folder)
            time_stamp = time_stamp.strip()
            time_stamp = time_stamp.split(' ')

            folder_name = time_stamp[-1]

            struct_time = time.strptime(folder_name, "%Y_%m_%d_%H_%M")

            time_with_folder.append([struct_time, folder_name])

        time_with_folder.sort(key=lambda x: x[0])

        last_item = time_with_folder[-1]

        return last_item[1]

    def load_new_datas(self):
        if self.item_folder_name != None :
            items = []

            for i in range(4):
                loaded_items = DataLoader().load_pickle_data(
                    filepath=self.absolute_path + 'database/datas/' + self.item_folder_name + '/process_' + str(
                        i + 1) + '.pkl')
                items += loaded_items

            # print(items)
            return items

        else :
            items = []

            for i in range(4) :
                loaded_items = DataLoader().load_pickle_data(filepath=self.absolute_path + 'database/datas/' + self.last_folder_name +'/process_' + str(i+1) + '.pkl')
                items += loaded_items

            #print(items)
            return items


    def load_main_item_db(self, version):
        try :
            loaded_data = DataLoader().load_pickle_data(filepath=self.absolute_path + 'database/main_item_db/' + 'main_item_db_ver_'+ str(version) + '.pkl')

        except :
            loaded_data = []
            DataLoader().save_pickle_data(data=loaded_data, filepath=self.absolute_path + 'database/main_item_db/' + 'main_item_db_ver_' + str(version))

        return loaded_data

    def merge(self, main_item_db, new_items):
        main_item_db += new_items

        while True :
            useless_item_found = False
            del_index = 0

            for idx, item in enumerate(main_item_db) :
                if item == ['item_name', 'info_list', 'image_link', 'main_category', 'sub_category', 'category_name']:
                    useless_item_found = True
                    del_index = idx
                    break

            del main_item_db[del_index]

            if useless_item_found == False :
                break

        str_item_db = []

        for item in main_item_db :
            str_item_db.append(json.dumps(item))

        str_item_db = set(str_item_db)

        filtered_data_list = []

        for item in str_item_db :
            filtered_data_list.append(json.loads(item))
            print(json.loads(item))

        print(filtered_data_list)

        print("-" * 50)
        print("Main Item DB Length : " + str(len(main_item_db)))
        print("Filtered Item DB Length : " + str(len(filtered_data_list)))
        print("Deleted data length : " + str(len(main_item_db) - len(filtered_data_list)))
        print("-" * 50)

        return filtered_data_list

class DataLoader():
    def __init__(self):
        pass

    def load_data_from_csv_multi_with_encode(self, filepath, encoding):
        all_datas = []

        f = open(filepath, 'r', encoding=encoding)
        rdr = csv.reader(f)
        for line in rdr:
            try:
                all_datas.append(line)
            except:
                pass
        f.close()

        return all_datas

    def write_data_in_csv_with_encode_multi(self, data_list, path, encoding):
        with open(path, 'w+', newline='', encoding=encoding) as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

            for data in data_list:
                writer.writerow(data)

    def save_hickle_data(self, data, filepath):
        print('Hickling data @', filepath)
        # filehandler = open(filepath, "wb")
        hickle.dump(data, filepath + '.hkl', mode='w')
        # pickle.dump(data, filehandler,protocol=4)
        # filehandler.close()

    def load_hickle_data(self, filepath):
        with open(filepath, 'r') as f:
            data = hickle.load(f)

        return data

    def save_pickle_data(self, data, filepath):
        print('Pickling data @', filepath)
        # filehandler = open(filepath, "wb")
        filehandler = open(filepath + '.pkl', "wb")
        pickle.dump(data, filehandler, protocol=4)
        # pickle.dump(data, filehandler,protocol=4)
        filehandler.close()

    def load_pickle_data(self, filepath):
        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        return data

class NaverCheckScraper():
    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list

        start_time = time.gmtime(time.time())

        self.starting_time = str(start_time.tm_year) + '_' + str(start_time.tm_mon) + '_' + str(
            start_time.tm_mday) + '_' + str(start_time.tm_hour) + '_' + str(start_time.tm_min)

        absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'

        self.front_url = 'https://search.shopping.naver.com/search/category?catId='
        self.mid_url = '&frm=NVSHCHK&origQuery&pagingIndex='
        self.back_url = '&pagingSize=40&productSet=checkout&query&sort=rel&timestamp=&viewType=list'

        loaded_category = DataLoader().load_data_from_csv_multi_with_encode(
            filepath=absolute_path + 'database/all_category.csv', encoding='utf8')

        self.category_data_list = []

        for category_data in loaded_category:
            self.category_data_list.append(
                {"main_category": category_data[0],
                 "sub_category": category_data[1],
                 "category_name": category_data[2],
                 "category_id": category_data[3]})

    def get_random_referrer(self):
        front_url = 'https://m.post.naver.com/viewer/postView.nhn?volumeNo='
        mid_url = '&memberNo='
        back_url = '&vType=VERTICAL'

        return front_url + str(randint(10000000, 99999999)) + mid_url + str(randint(10000000, 99999999)) + back_url

    def multi_get_data(self, num_of_process):
        with Manager() as manager :
            data_len_list = manager.list()

            if num_of_process == 2:
                basis = len(self.category_data_list) // 2

                process_1 = Process(target=self.get_data, args=(self.category_data_list, 0, basis * 1,data_len_list, 1))
                process_2 = Process(target=self.get_data, args=(
                self.category_data_list, basis * 1, basis * len(self.category_data_list),data_len_list, 2))

                process_1.start()
                process_2.start()

                process_1.join()
                process_2.join()

            if num_of_process == 3:
                basis = len(self.category_data_list) // 3

                process_1 = Process(target=self.get_data, args=(self.category_data_list, 0, basis * 1,data_len_list, 1))
                process_2 = Process(target=self.get_data,
                                    args=(self.category_data_list, basis * 1, basis * 2,data_len_list, 2))
                process_3 = Process(target=self.get_data,
                                    args=(
                                    self.category_data_list, basis * 2, basis * len(self.category_data_list),data_len_list, 3))

                process_1.start()
                process_2.start()
                process_3.start()

                process_1.join()
                process_2.join()
                process_3.join()

            elif num_of_process == 4:
                basis = len(self.category_data_list) // 4

                process_1 = Process(target=self.get_data, args=(self.category_data_list, 0, basis * 1,data_len_list, 1))
                process_2 = Process(target=self.get_data,
                                    args=(self.category_data_list, basis * 1, basis * 2,data_len_list, 2))
                process_3 = Process(target=self.get_data,
                                    args=(self.category_data_list, basis * 2, basis * 3,data_len_list, 3))
                process_4 = Process(target=self.get_data,
                                    args=(
                                    self.category_data_list, basis * 3, basis * len(self.category_data_list),data_len_list, 4))

                process_1.start()
                process_2.start()
                process_3.start()
                process_4.start()

                process_1.join()
                process_2.join()
                process_3.join()
                process_4.join()

    def get_info_data(self, category_data, driver):
        error_list = []
        extracted_list = []

        # Scroll down to bottom
        SCROLL_PAUSE_TIME = 0.3

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        template = driver.find_elements_by_xpath('//li[contains(@class, "basicList_item")]')

        for idx, element in enumerate(template):
            driver.execute_script("arguments[0].scrollIntoView();", element)
            #time.sleep(0.2)

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

            # Get Name
            item_name = element.find_element_by_xpath(
                xpath='descendant::div[contains(@class, "basicList_title")]/a').text

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
                        "main_category": category_data["main_category"], "sub_category": category_data["sub_category"],
                        "category_name": category_data["category_name"]}

            if data_set['image_link'] != None:
                extracted_list.append(data_set)

        #print(str(len(extracted_list)) + ' / 40')

        if len(extracted_list) <= 5 :
            print('Low than 40')
            print(driver.current_url)

        return {"extracted_list" : extracted_list, "error_list" : error_list}

    def save_error(self, process_num, errors):
        absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'

        error_log_list = DataLoader().load_data_from_csv_multi_with_encode(filepath=absolute_path + 'database/error_log/' + str(process_num) + '.csv', encoding='utf8')

        for e in errors :
            error_log_list.append(e)

        DataLoader().write_data_in_csv_with_encode_multi(data_list=error_log_list, path=absolute_path + 'database/error_log/' + str(process_num) + '.csv', encoding='utf8')

    def save_data_each(self, process_num, datas):
        absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'

        directory = absolute_path + 'database/datas/' + self.starting_time + '/'
        file_name = 'process_' + str(process_num)

        if not os.path.exists(directory):
            os.makedirs(directory)

        try :
            data_list = DataLoader().load_pickle_data(filepath=directory + file_name + '.pkl')

        except :
            data_list = []

        for item in datas:
            data_list.append(item)

        DataLoader().save_pickle_data(data=data_list, filepath=directory + file_name)

    def init_error_file(self, process_num):
        init_error_list = []

        absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'
        DataLoader().write_data_in_csv_with_encode_multi(data_list=init_error_list,
                                                         path=absolute_path + 'database/error_log/' + str(
                                                             process_num) + '.csv', encoding='utf8')

    def get_data(self, category_data_list, start_index, end_index, data_len_list, process_num):
        self.init_error_file(process_num=process_num)

        category_data_list = category_data_list[start_index:end_index]

        userAgent = self.user_agent_list[randint(0, len(self.user_agent_list))]


        options = Options()

        options.add_argument("enable-automation")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        options.add_argument(f'user-agent={userAgent}')
        
        absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'
        driver = webdriver.Chrome(absolute_path + 'driver/chromedriver', options=options)

        # Set the request header using the `header_overrides` attribute
        referrer_url = self.get_random_referrer()

        driver.header_overrides = {
            'Referer': referrer_url,
        }

        for category_data in category_data_list :
            # Set selenium option
            '''
            userAgent = self.user_agent_list[randint(0, len(self.user_agent_list))]

            options = Options()
            options.add_argument('--headless')
            options.add_argument(f'user-agent={userAgent}')
            
            profile = webdriver.FirefoxProfile()
            profile.set_preference('webdriver.load.strategy', 'unstable')

            driver = webdriver.Firefox(profile)
            driver.set_page_load_timeout(60)

            # Set the request header using the `header_overrides` attribute
            referrer_url = self.get_random_referrer()

            driver.header_overrides = {
                'Referer': referrer_url,
            }
            '''
            save_list = []

            for page_index in range(100):
                # Get data from url
                page_index += 1

                error_list = []

                if page_index % 10 == 0:
                    # Append data length
                    data_len_list.append(10)

                    # Print percent
                    all_length = 0

                    for i in data_len_list :
                        all_length += i

                    #print(str((all_length / len(self.category_data_list) / 8000) * 100) + '%')
                    print(str((all_length / len(self.category_data_list) / 100) * 100) + '%')

                    current_time = time.gmtime(time.time())
                    printing_time = str(current_time.tm_year) + '_' + str(current_time.tm_mon) + '_' + str(
                        current_time.tm_mday) + '_' + str(current_time.tm_hour) + '_' + str(current_time.tm_min)

                    print("Current Time : " + printing_time)
                    print("Started Time : " + self.starting_time)
                    print("Saved data : " + str(len(save_list)))

                    print("=" * 50)

                    # Save datas
                    if page_index != 0 :
                        self.save_data_each(process_num, save_list)
                        save_list = []

                try:
                    driver.get(url=self.front_url + category_data["category_id"] + self.mid_url + str(
                        page_index) + self.back_url)

                    error_with_data = self.get_info_data(category_data=category_data, driver=driver)

                    extracted_data = error_with_data["extracted_list"]
                    extracted_error = error_with_data["error_list"]

                    save_list += extracted_data
                    error_list += extracted_error

                except Exception as e:
                    print("전체 오류")
                    print(e)
                    error_list.append([e, "Outer"])

                self.save_error(process_num=process_num, errors=error_list)




if __name__ == '__main__':
    ua = UserAgent(
        fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')

    print("User Agent Loaded")

    user_agent_list = []

    for i in range(10000):
        user_agent_list.append(ua.random)

    # data_list = data_list[:len(data_list)//3]

    ncs = NaverCheckScraper(user_agent_list=user_agent_list)
    ncs.multi_get_data(num_of_process=4)

    # Merge data
    merger = MergeItems(item_folder_name=ncs.starting_time)

    loaded_db = merger.load_main_item_db(version=2)
    new_data = merger.load_new_datas()

    merged_items = merger.merge(main_item_db=loaded_db, new_items=new_data)
    DataLoader().save_pickle_data(data=merged_items,
                                  filepath=merger.absolute_path + 'database/main_item_db/' + 'main_item_db_ver_2')

    # 가장 최근이 아니라, 방금한 데이터를 Fetch