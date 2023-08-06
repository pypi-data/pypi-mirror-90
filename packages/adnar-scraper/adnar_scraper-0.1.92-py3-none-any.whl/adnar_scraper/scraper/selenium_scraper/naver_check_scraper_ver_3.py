import csv
from selenium import webdriver
import time
import regex as re
import hickle

from random import randint

from fake_useragent import UserAgent
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

from tbselenium.tbdriver import TorBrowserDriver

class DataLoader() :
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

class NaverCheckScraper() :
    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list

    def get_proxy_ip_list(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(chrome_options=options, executable_path='../driver/chromedriver (2).exe')
        driver.get("https://sslproxies.org/")
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
        ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(
            EC.visibility_of_all_elements_located((By.XPATH,
                                                   "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
        ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(
            EC.visibility_of_all_elements_located((By.XPATH,
                                                   "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
        driver.quit()
        proxies = []
        for i in range(0, len(ips)):
            proxies.append(ips[i] + ':' + ports[i])
        print(proxies)

        return proxies

    def get_random_referrer(self):
        front_url = 'https://m.post.naver.com/viewer/postView.nhn?volumeNo='
        mid_url = '&memberNo='
        back_url = '&vType=VERTICAL'

        return front_url + str(randint(10000000, 99999999)) + mid_url + str(randint(10000000, 99999999)) + back_url

    def multi_get_data(self, data_list, num_of_process):
        with Manager() as manager :
            save_list = manager.list()

            if num_of_process == 3 :
                basis = len(data_list) // 3

                process_1 = Process(target=self.get_data, args=(data_list, 0, basis * 1, save_list))
                process_2 = Process(target=self.get_data, args=(data_list, basis * 1, basis * 2, save_list))
                process_3 = Process(target=self.get_data, args=(data_list, basis * 2, basis * len(data_list), save_list))

                process_1.start()
                process_2.start()
                process_3.start()

                process_1.join()
                process_2.join()
                process_3.join()

            elif num_of_process == 4 :
                basis = len(data_list) // 4

                process_1 = Process(target=self.get_data, args=(data_list, 0, basis * 1, save_list))
                process_2 = Process(target=self.get_data, args=(data_list, basis * 1, basis * 2, save_list))
                process_3 = Process(target=self.get_data, args=(data_list, basis * 2, basis * 3, save_list))
                process_4 = Process(target=self.get_data, args=(data_list, basis * 3, basis * len(data_list), save_list))

                process_1.start()
                process_2.start()
                process_3.start()
                process_4.start()

                process_1.join()
                process_2.join()
                process_3.join()
                process_4.join()

            '''
            basis = len(data_list) // num_of_process
            process_list = []
            
            for i in range(num_of_process) :
                if i == 0 :
                    process = Process(target=self.get_data, args=(data_list, 0, basis * i+1, save_list))
                    process.start()
                    process_list.append(process)

                elif 0 < i < (num_of_process - 1) :
                    process = Process(target=self.get_data, args=(data_list, basis * i, basis * i+1, save_list))
                    process.start()
                    process_list.append(process)

                else :
                    process = Process(target=self.get_data, args=(data_list, basis * i, basis * len(data_list), save_list))
                    process.start()
                    process_list.append(process)


            for process in process_list :
                process.join()
            '''
            save_list = list(save_list)
            print(str(len(save_list)) + '개입니다.')
            self.save_data(save_list=save_list)

            '''
                        
                        '''

    def save_data(self, save_list) :

        print(str(save_list) + '개')

        current_time = time.gmtime(time.time())
        file_name = str(current_time.tm_year) + '_' + str(current_time.tm_mon) + '_' + str(
            current_time.tm_mday) + '_' + str(current_time.tm_hour) + '_' + str(current_time.tm_min)
        DataLoader().save_hickle_data(data=save_list, filepath=absolute_path + 'database/base/items/' + file_name)

    def data_from_smart_store(self, data, driver, current_index, data_length):
        try:
            print(str(int(current_index / data_length * 100)) + '%')
            # time.sleep(0.5)

            item_data = {"category": data[0], "main_category": data[1], "sub_category": data[2], "item_name": None,
                         "attributes": None, "tags": None, "image_url": None}

            item_name = driver.find_element_by_xpath(xpath='//dt[contains(@class, "prd_name")]/strong').text
            image_url = driver.find_element_by_xpath(xpath='//img[contains(@alt, "대표이미지")]').get_attribute('src')

            # Get attributes
            template = driver.find_elements_by_xpath('//table[contains(@class, "tb_view2")]/tbody')

            info_template = template[1]

            items = info_template.find_elements_by_xpath('descendant::span')

            attribute_name = []
            attribute_value = []

            for idx, item in enumerate(items):
                # link_template = element.xpath('descendant::a')
                if idx % 2 == 0:
                    attribute_name.append(item.text)
                else:
                    attribute_value.append(item.text)

            attributes = []

            for idx, name in enumerate(attribute_name):
                value = attribute_value[idx]

                attributes.append({name: value})

            # Get Tags
            tag_list = driver.find_elements_by_xpath('//div[contains(@class, "goods_tag")]/ul/li/a')

            tags = []

            for tag_item in tag_list:
                tags.append(re.sub(pattern="#", repl="", string=tag_item.text))

            # Make it to data form
            item_data["item_name"] = item_name
            item_data["image_url"] = image_url
            item_data["attributes"] = attributes
            item_data["tags"] = tags

            return item_data

        except Exception as e:
            print(data[3])
            print(e)

    def data_from_outlet_window(self, data, driver, current_index, data_length):
        try:
            print(str(int(current_index / data_length * 100)) + '%')
            # time.sleep(0.5)

            item_data = {"category": data[0], "main_category": data[1], "sub_category": data[2], "item_name": None,
                         "attributes": None, "tags": None, "image_url": None}

            item_name = driver.find_element_by_xpath(xpath='/html/body/div/div/div[2]/div[2]/div[2]/div[2]/fieldset/div[1]/h3').text
            image_url = driver.find_element_by_xpath(xpath='/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/img').get_attribute('src')

            # Get attributes
            template = driver.find_elements_by_xpath('/html/body/div/div/div[2]/div[2]/div[8]/div[2]/table/tbody/tr')

            attributes = []

            for item in template :
                temp_name_list = item.find_elements_by_xpath('descendant::th')
                temp_value_list = item.find_elements_by_xpath('descendant::td')

                for idx, name_tag in enumerate(temp_name_list) :
                    name = name_tag.text
                    value = temp_value_list[idx].text

                    attributes.append({name: value})

            # Get Tags
            tag_list_parent = driver.find_element_by_xpath(xpath="//strong[text()[contains(.,'관련 태그')]]/..")
            tag_list = tag_list_parent.find_elements_by_xpath('descendant::ul/li/a')
            tags = []

            for tag_item in tag_list:
                tags.append(re.sub(pattern="#", repl="", string=tag_item.text))

            # Make it to data form
            item_data["item_name"] = item_name
            item_data["image_url"] = image_url
            item_data["attributes"] = attributes
            item_data["tags"] = tags

            return item_data

        except Exception as e:
            print(data[3])
            print(e)

    # No-product, No-element, Not-naver

    def create_proxy_address(self):
        pass


    def get_data(self, data_list, start_index, end_index, save_list) :
        data_list = data_list[start_index:end_index]

        data_length = len(data_list)

        for i in range(len(data_list)//30) :
            if (i+1) * 30 <= len(data_list) :
                # Set User agent & referrer
                userAgent =  self.user_agent_list[randint(0, len(self.user_agent_list))]
                #proxies = self.get_proxy_ip_list()

                options = Options()
                #options.add_argument('--headless')
                options.add_argument(f'user-agent={userAgent}')

                # Set Tor Browser to switch IP
                with TorBrowserDriver("/home/discoverious/Documents/tor-browser-linux64-9.5.3_en-US/tor-browser_en-US/") as driver:
                    # Set the request header using the `header_overrides` attribute
                    referer_url = self.get_random_referrer()

                    driver.header_overrides = {
                        'Referer': referer_url,
                    }

                    # rotate in 30 to avoid "Too many request"
                    for item_index in range((i*30), ((i+1) * 30)) :
                        data = data_list[item_index]
                        url = data[3]

                        try:
                            driver.get(url=url)
                            current_url = driver.current_url

                            if re.search(pattern='no-product', string=current_url) is not None:
                                print("Deleted Item")

                            elif re.search(pattern='outlet', string=current_url) is not None:
                                extracted_data = self.data_from_outlet_window(data=data, driver=driver, current_index=item_index,
                                                                              data_length=data_length)
                                save_list.append(extracted_data)

                            elif re.search(pattern='smartstore', string=current_url) is not None:
                                extracted_data = self.data_from_smart_store(data=data, driver=driver, current_index=item_index,
                                                                            data_length=data_length)
                                save_list.append(extracted_data)

                            else:
                                print("Not Naver store")

                        except Exception as e:
                            print("전체 오류")
                            print(e)

                        print("=" * 50)

                    driver.close()

if __name__ == '__main__' :
    ua = UserAgent(fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')

    user_agent_list = []

    for i in range(10000) :
        user_agent_list.append(ua.random)

    absolute_path = '/home/discoverious/Documents/PycharmProjects/seo_scraper/'
    
    data_list = DataLoader().load_data_from_csv_multi_with_encode(
        filepath=absolute_path + 'database/base/all_items/2020_8_7_11_0.csv', encoding='utf8')
    del data_list[0]

    print(len(data_list))

    #data_list = data_list[:len(data_list)//3]

    ncs = NaverCheckScraper(user_agent_list=user_agent_list)
    ncs.multi_get_data(data_list=data_list, num_of_process=3)

    #DataLoader().load_hickle_data(filepath=absolute_path + 'database/base/items/2020_8_7_6_8')
    # 오후 5시 시작 그 다음날 3시 8분 끝
