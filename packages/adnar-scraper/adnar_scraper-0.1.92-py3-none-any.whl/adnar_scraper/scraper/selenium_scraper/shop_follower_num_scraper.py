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
import re


class ShopFollowerNumScraper:
    def __init__(self):
        self.scraper_name = "shop_follower_info_scraper"
        self.kind = "local_shop"

        self.selenium_controller = SeleniumController()
        self.starting_time = DataLoader.create_file_name()
        self.save_file_controller = SaveFileController(name=self.scraper_name, date_time=self.starting_time,
                                                       kind=self.kind)
        self.database_controller = DatabaseController(selected_database=self.kind)

    def get_shop_follower_num_and_graph(self, shop_data_list, min_num, max_num):
        driver = self.selenium_controller.get_image_blocked_driver(show_browser=False)

        shop_data_dict = dict()
        error_shop_dict = {"follower_error": [], "graph_error": []}

        for shop_idx, shop_data in enumerate(shop_data_list):
            print(f"{round(shop_idx / len(shop_data_list) * 100, 3)}%")
            print(f"https://{shop_data['url']}/profile")
            driver.get(f"https://{shop_data['url']}/profile")

            # Define dict for each shop
            each_shop_dict = {'follower': None, 'age': dict(), 'gender': {'male': None, 'female': None}}

            # Get num of follower
            try:
                # For version 1
                num_of_follower = driver.find_element_by_xpath(xpath='//*[@id="container"]/div[1]/div/div[1]/div[1]/div/div/button/span[3]/span').text
                num_of_follower = int(re.sub(pattern='\,', repl='', string=num_of_follower))

            except Exception as e:
                try:
                    # For version 2
                    num_of_follower = driver.find_element_by_xpath(xpath='//*[@id="header"]/div/div[2]/div[1]').text
                    num_of_follower = int(re.sub(pattern='스토어찜 |\,', repl='', string=num_of_follower))

                except Exception as e_2:
                    try:
                        # For version 3
                        num_of_follower = driver.find_element_by_xpath(xpath='//*[@id="container"]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/button/span[3]/span').text
                        num_of_follower = int(re.sub(pattern='\,', repl='', string=num_of_follower))

                    except Exception as e_end:
                        try:
                        # For Deleted market
                            num_of_follower = None
                            end_string = driver.find_element_by_xpath(
                                xpath='//*[@id="MAIN_CONTENT_ROOT_ID"]/div/div[2]/div[2]/h2/em').text

                            if re.search(pattern='찾을 수 없습니다.', string=end_string) is not None:
                                continue

                        except:
                            error_shop_dict["follower_error"].append(shop_data)
                            continue

            try:
                each_shop_dict['follower'] = num_of_follower
                print(f"Follower : {num_of_follower}")
                print('-')

                # Get Age Graph
                graph_list = driver.find_elements_by_xpath(xpath="/html/body/div/div/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li")

                for each_graph in graph_list:
                    age = int(each_graph.find_element_by_xpath(xpath='div[2]').text)
                    age_ratio = int(float(each_graph.find_element_by_xpath(xpath='descendant::div[1]/div/span').text))

                    each_shop_dict['age'][str(age)] = age_ratio
                    print(f"Age : {age}, ratio : {age_ratio}")

                # Get Gender Graph
                male_ratio = 0
                female_ratio = 0

                gender_graph_list = driver.find_elements_by_xpath(
                    xpath='/html/body/div/div/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div')

                for each_gender_graph in gender_graph_list:
                    gender_ratio = int(re.sub(pattern='%',
                                              string=each_gender_graph.find_element_by_xpath(xpath='span/div').text,
                                              repl=''))

                    style_information = each_gender_graph.find_element_by_xpath(xpath='span').get_attribute(name='style')
                    if re.search(pattern='rgb\(120, 193, 255\)', string=style_information) is not None:
                        # Male text color
                        male_ratio = gender_ratio

                    else:
                        female_ratio = gender_ratio

                each_shop_dict['gender']['male'] = male_ratio
                each_shop_dict['gender']['female'] = female_ratio

                print('-')
                print(f"Male: {male_ratio}, Female: {female_ratio}")

                shop_data_dict[shop_data['name']] = each_shop_dict
                print(shop_data_dict[shop_data['name']])

                print("=" * 50)

            except:
                error_shop_dict["graph_error"].append(shop_data)

        self.save_file_controller.save_with_string_path(string=f"{min_num}_to_{max_num}",
                                                        data_set=shop_data_dict)

        return error_shop_dict

if __name__ == "__main__":
    from adnar_scraper.settings import LINUX_SHOP_DATABASE_PATH

    scraper = ShopFollowerNumScraper()

    shop_datas = DatabaseController('local_shop').get_recent_data(db_name='shop_filterer')
    #shop_datas = [{"url":"shopping.naver.com/outlink"}]
    error_shop_datas = scraper.get_shop_follower_num_and_graph(shop_data_list=shop_datas, min_num=20, max_num=300)

    error_name = DataLoader.create_file_name()

    path = LINUX_SHOP_DATABASE_PATH + 'shop_follower_error/'
    DataLoader.create_if_folder_not_exists(path=path)

    DataLoader.save_pickle_data(data=error_shop_datas, file_path=path + DataLoader.create_file_name())