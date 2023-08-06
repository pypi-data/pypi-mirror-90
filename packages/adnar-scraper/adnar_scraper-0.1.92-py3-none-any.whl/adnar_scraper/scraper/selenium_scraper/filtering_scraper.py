from preprocessor.data_loader import DataLoader
from selenium import webdriver
import time
import regex as re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process, Manager
from selenium.webdriver.chrome.options import Options
import os
from random import randint
from fake_useragent import UserAgent

class FilteringScraper() :
    # 데이터의 어디가 얼마만큼이나 됐고, 어디까지 되었는가

    def __init__(self, user_agent_list, cat_list, cat_num, save_version, by_category=None, category_name=None):
        self.save_version = save_version

        self.user_agent_list = user_agent_list

        self.absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'

        self.front_url = 'https://search.shopping.naver.com/search/category?catId='
        self.mid_url = '&frm=NVSHCHK&origQuery&pagingIndex='
        self.back_url = '&pagingSize=40&productSet=checkout&query&sort=rel&timestamp=&viewType=list'

        if by_category == True :
            self.cat_list = cat_list
            self.cat_num = str(cat_num)
            self.filter_element_list = DataLoader().load_pickle_data(
                filepath='../database/splited_filter_element_list/' + self.cat_list + '_' + self.cat_num + '.pkl')

            filtered_by_category = []

            for categories in self.filter_element_list :
                if categories["category_name"] == category_name :
                    filtered_by_category.append(categories)

            self.filter_element_list = filtered_by_category

        else :
            self.cat_list = cat_list
            self.cat_num = str(cat_num)
            self.filter_element_list = DataLoader().load_pickle_data(
                filepath='../database/splited_filter_element_list/' + self.cat_list + '_' + self.cat_num + '.pkl')

        print(self.filter_element_list)

        start_time = time.gmtime(time.time())

        self.starting_time = str(start_time.tm_year) + '_' + str(start_time.tm_mon) + '_' + str(
            start_time.tm_mday) + '_' + str(start_time.tm_hour) + '_' + str(start_time.tm_min)

    def multi_get_data(self, num_of_process):
        with Manager() as manager :
            data_len_list = manager.list()

            if num_of_process == 2:
                basis = len(self.filter_element_list) // 2

                process_1 = Process(target=self.get_data, args=(0, basis * 1,data_len_list, 1))
                process_2 = Process(target=self.get_data, args=(
                basis * 1, basis * len(self.filter_element_list),data_len_list, 2))

                process_1.start()
                process_2.start()

                process_1.join()
                process_2.join()

            if num_of_process == 3:
                basis = len(self.filter_element_list) // 3

                process_1 = Process(target=self.get_data, args=(0, basis * 1,data_len_list, 1))
                process_2 = Process(target=self.get_data,
                                    args=(basis * 1, basis * 2,data_len_list, 2))
                process_3 = Process(target=self.get_data,
                                    args=(
                                    basis * 2, basis * len(self.filter_element_list),data_len_list, 3))

                process_1.start()
                process_2.start()
                process_3.start()

                process_1.join()
                process_2.join()
                process_3.join()

            elif num_of_process == 4:
                basis = len(self.filter_element_list) // 4

                process_1 = Process(target=self.get_data, args=(0, basis * 1,data_len_list, 1))
                process_2 = Process(target=self.get_data,
                                    args=(basis * 1, basis * 2,data_len_list, 2))
                process_3 = Process(target=self.get_data,
                                    args=(basis * 2, basis * 3,data_len_list, 3))
                process_4 = Process(target=self.get_data,
                                    args=(
                                    basis * 3, basis * len(self.filter_element_list),data_len_list, 4))

                process_1.start()
                process_2.start()
                process_3.start()
                process_4.start()

                process_1.join()
                process_2.join()
                process_3.join()
                process_4.join()

    def save_error(self, process_num, errors):
        absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'

        error_log_list = DataLoader().load_data_from_csv_multi_with_encode(filepath=absolute_path + 'database/error_log/filtering_scraper/' + str(process_num) + '.csv', encoding='utf8')

        for e in errors :
            error_log_list.append(e)

        DataLoader().write_data_in_csv_with_encode_multi(data_list=error_log_list, path=absolute_path + 'database/error_log/filtering_scraper/' + str(process_num) + '.csv', encoding='utf8')

    def save_data_each(self, process_num, datas):
        absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'

        directory = absolute_path + 'database/full_datas/ver_'+ str(self.save_version) + '/' + self.cat_list + '/' + self.cat_num + '/' + self.starting_time + '/'
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
                                                         path=absolute_path + 'database/error_log/filtering_scraper/' + str(
                                                             process_num) + '.csv', encoding='utf8')

    def get_tag_in_new_tab(self, driver, item_url):
        # Switch to new tab
        driver.execute_script("window.open('')")
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        driver.switch_to_window(driver.window_handles[-1])
        driver.get(item_url)

        # Get Tags
        tags = []

        try :
            tag_list = driver.find_elements_by_xpath('//div[contains(@class, "goods_tag")]/ul/li/a')

            for tag_item in tag_list:
                tags.append(re.sub(pattern="#", repl="", string=tag_item.text))

        except Exception as e :
            print(e)

        # Switch focus to old tab and close opened tab
        driver.close()
        driver.switch_to_window(driver.window_handles[0])

        return tags

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

            # Get Name & Item URL
            item_basic_info = element.find_element_by_xpath(
                xpath='descendant::div[contains(@class, "basicList_title")]/a')

            item_name = item_basic_info.text
            item_url = item_basic_info.get_attribute('href')

            tag_data = self.get_tag_in_new_tab(driver=driver, item_url=item_url)

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
            data_set = {'item_name': item_name, 'info_list': filtered_info_list, 'image_link': image_link, 'tag_data': tag_data,
                        "main_category": category_data["main_category"], "sub_category": category_data["sub_category"],
                        "category_name": category_data["category_name"]}

            if data_set['image_link'] != None:
                extracted_list.append(data_set)

        #print(str(len(extracted_list)) + ' / 40')

        if len(extracted_list) <= 5 :
            print('Low than 40')
            print(driver.current_url)

        return {"extracted_list" : extracted_list, "error_list" : error_list}

    def get_data(self, start_index, end_index, data_len_list, process_num):
        print('Initiate Get data')
        self.init_error_file(process_num=process_num)

        for filter_element in self.filter_element_list[start_index:end_index] :
            for element_name in filter_element["filter_element"] :
                url = self.front_url + filter_element['category_id'] + self.mid_url + str(1) + self.back_url

                userAgent = self.user_agent_list[randint(0, len(self.user_agent_list))]

                options = Options()

                options.add_argument("start-maximized")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-infobars")
                options.add_argument("--disable-browser-side-navigation")
                options.add_argument("enable-automation")
                options.add_argument("--headless")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-extensions")
                options.add_argument("--dns-prefetch-disable")
                options.add_argument("--disable-gpu")
                options.add_argument(f'user-agent={userAgent}')

                driver = webdriver.Chrome(self.absolute_path + 'driver/chromedriver', options=options)

                driver.get(url)

                try :

                    filter_name_tag = driver.find_element_by_xpath(
                        '//div[contains(text(), "' + filter_element["filter_name"] + '") and contains(@class, "filter_finder_tit")]')

                    if re.search(pattern='더보기', string=filter_name_tag.text) is not None:
                        try :
                            filter_name_tag.find_element_by_xpath('descendant::button').click()

                        except :
                            filter_name_tag.find_element_by_xpath('descendant::a').click()

                    tag_parent = filter_name_tag.find_element_by_xpath('..')

                    element_list = tag_parent.find_elements_by_xpath('descendant::ul/li')#[contains(text(),"'+ element_name + '")]')

                    for element in element_list :
                        if element.text == element_name :
                            try :
                                element.find_element_by_xpath(xpath='descendant::button').click()

                            except :
                                element.find_element_by_xpath(xpath='descendant::a').click()

                    time.sleep(2)

                    page_button_tag = None

                    try :
                        page_button_tag = driver.find_element_by_xpath('//button[contains(text(), "전체") and contains(@class, "subFilter_filter")]')

                    except :
                        page_button_tag = driver.find_element_by_xpath('//a[contains(text(), "전체") and contains(@class, "subFilter_filter")]')


                    total_item_length = int(re.sub(pattern=',', repl='', string=page_button_tag.find_element_by_xpath('descendant::span[contains(@class,"subFilter_num_")]').text))

                    print(total_item_length)

                    splited_url = driver.current_url.split("pagingIndex=1")
                    print(splited_url)

                    page_length = total_item_length // 40

                    save_list = []

                    error_list = []

                    if page_length == 0 and total_item_length != 0 :
                        url = splited_url[0] + 'pagingIndex=' + str(1) + splited_url[1]
                        # get item code
                        self.get_item_data(process_num=process_num, error_list=error_list,
                                           page_length=page_length, data_len_list=data_len_list, save_list=save_list,
                                           page=1, url=url, driver=driver,
                                           category_data={"main_category": filter_element["main_category"],
                                                          "sub_category": filter_element["sub_category"],
                                                          "category_name": filter_element["category_name"]})

                    else :
                        if total_item_length % 40 == 0 :
                            for page in range(page_length):
                                page = page + 1

                                url = splited_url[0] + 'pagingIndex=' + str(page) + splited_url[1]
                                # get item code
                                self.get_item_data(process_num=process_num, error_list=error_list,
                                                   page_length=page_length, data_len_list=data_len_list, save_list=save_list, page=page, url=url, driver=driver,
                                                   category_data={"main_category": filter_element["main_category"], "sub_category": filter_element["sub_category"],
                            "category_name": filter_element["category_name"]})
                        else :
                            current_page = 0

                            for page in range(page_length) :
                                if page <= 199 :
                                    page = page + 1
                                    current_page = page

                                    url = splited_url[0] + 'pagingIndex=' + str(page) + splited_url[1]
                                    # get item code
                                    self.get_item_data(process_num=process_num, error_list=error_list,
                                                       page_length=page_length, data_len_list=data_len_list, save_list=save_list, page=page, url=url, driver=driver,
                                                       category_data={"main_category": filter_element["main_category"],
                                                                      "sub_category": filter_element["sub_category"],
                                                                      "category_name": filter_element["category_name"]}
                                                       )

                            current_page += 1

                            if current_page <= 199 :
                                url = splited_url[0] + 'pagingIndex=' + str(current_page) + splited_url[1]
                                # get item code
                                self.get_item_data(process_num=process_num, error_list=error_list,
                                                   page_length=page_length, data_len_list=data_len_list, save_list=save_list, page=current_page, url=url, driver=driver,
                                                   category_data={"main_category": filter_element["main_category"],
                                                                  "sub_category": filter_element["sub_category"],
                                                                  "category_name": filter_element["category_name"]}
                                                   )

                    driver.close()

                except Exception as e :
                    print("Finding Button Error")
                    print(e)

    def get_item_data(self, process_num, error_list, page_length, data_len_list, save_list, page, url, driver, category_data):
        if page % 10 == 0:
            # Append data length
            data_len_list.append(10 / page_length)

            # Print percent
            all_length = 0

            for i in data_len_list:
                all_length += i

            # print(str((all_length / len(self.category_data_list) / 8000) * 100) + '%')
            print(str((all_length / len(self.filter_element_list)) * 100) + '%')

            current_time = time.gmtime(time.time())
            printing_time = str(current_time.tm_year) + '_' + str(current_time.tm_mon) + '_' + str(
                current_time.tm_mday) + '_' + str(current_time.tm_hour) + '_' + str(current_time.tm_min)

            print("Current Time : " + printing_time)
            print("Started Time : " + self.starting_time)
            print("Saved data : " + str(len(save_list)))
            print("=" * 50)

            # Save datas
            if page != 0:
                self.save_data_each(process_num, save_list)
                save_list = []

        try:
            driver.get(url=url)
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

    def get_each_filter_element(self):
        filter_category = DataLoader().load_pickle_data(filepath=self.absolute_path + 'database/filter_list.pkl')
        driver = webdriver.Chrome(self.absolute_path + 'driver/chromedriver')

        save_item_list = []

        for category_data in filter_category:
            url = self.front_url + category_data['category_id'] + self.mid_url + str(1) + self.back_url
            driver.get(url)

            for filter_item in category_data["filter_list"]:
                element_list = []
                # Check if in stop_words
                filter_name_tag = driver.find_element_by_xpath('//div[contains(text(), "' + filter_item + '") and contains(@class, "filter_finder_tit")]')

                if re.search(pattern='더보기', string=filter_name_tag.text) is not None :
                    filter_name_tag.find_element_by_xpath('descendant::button').click()

                tag_parent = filter_name_tag.find_element_by_xpath('..')

                element_items = tag_parent.find_elements_by_xpath('descendant::ul[contains(@class, "filter_finder")]/li')

                for element in element_items :
                    element_list.append(element.text)

                print("=" * 50)

                save_item = {"main_category": category_data["main_category"],
                 "sub_category": category_data["sub_category"],
                 "category_name": category_data["category_name"],
                 "category_id": category_data["category_id"],
                 "filter_name": filter_item,
                 "filter_element": element_list}

                save_item_list.append(save_item)

            print("*" * 50)

        DataLoader().save_pickle_data(data=save_item_list, filepath='../database/filter_element_list')
            

    def get_each_category_filter(self):
        stop_words = ['카테고리', '브랜드', '가격', '배송/혜택/색상']

        self.absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'
        
        loaded_category = DataLoader().load_data_from_csv_multi_with_encode(
            filepath=self.absolute_path + 'database/all_category.csv', encoding='utf8')

        category_data_list = []

        for category_data in loaded_category:
            category_data_list.append(
                {"main_category": category_data[0],
                 "sub_category": category_data[1],
                 "category_name": category_data[2],
                 "category_id": category_data[3],
                 "filter_list": None})

        self.absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'
        driver = webdriver.Chrome(self.absolute_path + 'driver/chromedriver')

        for category_data in category_data_list :
            url = self.front_url + category_data['category_id'] + self.mid_url + str(1) + self.back_url
            driver.get(url)

            filter_name_tag_list = driver.find_elements_by_xpath('//div[contains(@class, "filter_finder_tit")]')

            filter_list = []

            for filter_name_tag in filter_name_tag_list :
                # Check if in stop_words
                filter_name = re.sub(string=filter_name_tag.text, repl='', pattern='더보기|접기').strip()

                is_in_stopwords = False

                for stop_word in stop_words :
                    if stop_word == filter_name :
                        is_in_stopwords = True
                        break

                if is_in_stopwords == False :
                    filter_list.append(filter_name)

            category_data["filter_list"] = filter_list

        DataLoader().save_pickle_data(data=category_data_list, filepath='../database/filter_list')

if __name__ == "__main__" :
    cat_list = ['남성의류', '여성언더웨어_잠옷', '남성언더웨어_잠옷', '여성의류']

    cat_list_1 = ['남성언더웨어_잠옷', '여성언더웨어_잠옷']
    cat_list_2 = ['여성언더웨어_잠옷', '남성언더웨어_잠옷']
    cat_list_3 = ['남성의류', '여성의류']
    cat_list_4 = ['여성의류', '남성의류']

    cat_list_5 = ['남성의류']
    cat_list_6 = ['여성의류']
    cat_list_7 = ['남성언더웨어_잠옷']
    cat_list_8 = ['여성언더웨어_잠옷']

    by_category = True
    wanted_categories = ['티셔츠', '니트/스웨터']

    save_version = 2

    if by_category == True :
        for cat in cat_list_5 :
            for category in wanted_categories :
                for i in range(3) :
                    order = i + 1

                    ua = UserAgent(
                        fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')

                    print("User Agent Loaded")

                    user_agent_list = []

                    for i in range(10000):
                        user_agent_list.append(ua.random)

                    fs = FilteringScraper(user_agent_list=user_agent_list, cat_list=cat, cat_num=order, by_category=by_category, category_name=category, save_version=save_version)

                    if len(fs.filter_element_list) == 1 :
                        fs.get_data(start_index=0, end_index=1, data_len_list=[], process_num=1)

                    elif len(fs.filter_element_list) == 2 :
                        fs.multi_get_data(2)

                    elif len(fs.filter_element_list) == 3 :
                        fs.multi_get_data(3)

                    elif len(fs.filter_element_list) >= 4 :
                        fs.multi_get_data(4)



    if by_category == False:
        for cat in cat_list_4:
            for i in range(3):
                order = i + 1

                ua = UserAgent(
                    fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')

                print("User Agent Loaded")

                user_agent_list = []

                for i in range(10000):
                    user_agent_list.append(ua.random)

                fs = FilteringScraper(user_agent_list=user_agent_list, cat_list=cat, cat_num=order,
                                      by_category=False, save_version=save_version)

                fs.multi_get_data(4)

    '''
    #

    data = DataLoader().load_pickle_data('../database/filter_element_list.pkl')

    length = 0
    db = []

    cat_list = ['남성의류', '여성언더웨어/잠옷', '남성언더웨어/잠옷', '여성의류']

    category_name = cat_list[3] #여성언더웨어/잠옷, 남성언더웨어/잠옷, 남성의

    for d in data :
        if d['sub_category'] == category_name :
            length += 1
            db.append(d)

    splited_db_1 = db[0:length//3*1]
    splited_db_2 = db[length//3*1:length//3*2]
    splited_db_3 = db[length//3*2:length]

    for k in splited_db_1 :
        print(k)

    print("=" * 20)

    for k in splited_db_2 :
        print(k)

    print("=" * 20)

    for k in splited_db_3 :
        print(k)


    category_name = re.sub(pattern='/', repl="_", string=category_name)

    DataLoader().save_pickle_data(data=splited_db_1,
                                  filepath='../database/splited_filter_element_list/' + category_name + '_1')
    DataLoader().save_pickle_data(data=splited_db_2,
                                  filepath='../database/splited_filter_element_list/' + category_name + '_2')
    DataLoader().save_pickle_data(data=splited_db_3,
                                  filepath='../database/splited_filter_element_list/' + category_name + '_3')
    '''




