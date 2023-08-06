from PIL import Image
import numpy as np
from multiprocessing import Process, Manager
import requests

from adnar_scraper import settings
from adnar_scraper.utility.database_controller import DatabaseController
from adnar_scraper.utility.item_analyzer import ItemAnalyzer
from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper.utility.save_file_controller import SaveFileController
from adnar_scraper.utility.error_file_controller import ErrorFileController


class NaverImageScraper:
    def __init__(self, data_list, full_data_length, category_name):
        self.scraper_name = "naver_image_scraper"
        self.kind = "item"

        self.starting_time = DataLoader.create_file_name()
        self.save_file_controller = SaveFileController(name=self.scraper_name,
                                                       date_time=category_name + '/' + self.starting_time,
                                                       kind=self.kind)

        self.data_list = data_list
        self.error_file_controller = ErrorFileController(name=self.scraper_name, date_time=category_name + '/' + self.starting_time)

        self.formal_percent = 0

        self.full_data_length = full_data_length

    def get_image(self, start_index, end_index, save_list, process_num):
        print('Process ' + str(process_num)  + ' Activated')
        self.error_file_controller.init_error_file(process_num=process_num)

        image_data_list = []
        error_list = []

        print(start_index)
        print(end_index)

        for idx, data in enumerate(self.data_list[start_index:end_index]):
            try :
                if save_list[0]/len(self.data_list) * 100 > self.formal_percent:
                    print("*" * 100)
                    print(str(save_list[0]/self.full_data_length * 100) + '%')
                    self.formal_percent += 1
                    print("*" * 100)

                image_size = (32, 32)

                image = Image.open(requests.get(data['image_link'], stream=True).raw)
                resized_image = image.resize(image_size, Image.ANTIALIAS)
                image_array = np.asarray(resized_image)

                data['image_file'] = image_array

                save_list[0] += 1
                image_data_list.append(data)

                if len(image_data_list) >= 100 and idx <= (len(self.data_list[start_index:end_index]) -1) - 100 :
                    print("Process_" + str(process_num) + ' : ' + str(len(image_data_list)) + ' data saved')
                    self.save_file_controller.save_data_memory_saving_version(process_num=process_num,
                                                                              data_set=image_data_list)
                    image_data_list = []

            except Exception as e:
                print(e)
                error_list.append(e)

                self.error_file_controller.save_error(process_num=process_num, errors=error_list)

                error_list = []

            if idx == len(self.data_list[start_index:end_index]) - 1:
                self.save_file_controller.save_data_memory_saving_version(process_num=process_num,
                                                                          data_set=image_data_list)

        return save_list

    def multi_get_image(self, num_of_process):
        with Manager() as manager:
            save_list = manager.list()
            save_list.append(0)

            if num_of_process is 2:
                basis = len(self.data_list) // 2

                process_1 = Process(target=self.get_image,
                                    args=(0, basis * 1, save_list, 1))
                process_2 = Process(target=self.get_image,
                                    args=(basis * 1, len(self.data_list), save_list, 2))

                process_1.start()
                process_2.start()

                process_1.join()
                process_2.join()

                save_list = list(save_list)
                print(str(save_list[0]) + '개 입니다.')

            elif num_of_process is 4:
                basis = len(self.data_list) // 4

                process_1 = Process(target=self.get_image,
                                    args=(0, basis * 1, save_list, 1))
                process_2 = Process(target=self.get_image,
                                    args=(basis * 1, basis * 2, save_list, 2))
                process_3 = Process(target=self.get_image,
                                    args=(basis * 2, basis * 3, save_list, 3))
                process_4 = Process(target=self.get_image,
                                    args=(basis * 3, basis * len(self.data_list), save_list, 4))

                process_1.start()
                process_2.start()
                process_3.start()
                process_4.start()

                process_1.join()
                process_2.join()
                process_3.join()
                process_4.join()

                save_list = list(save_list)
                print(str(save_list[0]) + '개 입니다.')

if __name__ == "__main__":
    datas = DataLoader.load_pickle_data(file_path='E:/databases/ver_1/local_database/item_database/separated_category_items/패션의류&여성의류&티셔츠.pkl')

    scraper = NaverImageScraper(data_list=datas, full_data_length=len(datas))
    scraper.multi_get_image(num_of_process=4)

    '''
    database_controller = DatabaseController(selected_database='item')

    splited_file_path_list = database_controller.get_splited_data_path(
        db_name=settings.ITEM_DATABASE_PATH + 'shop_detail_scraper',
        split_rank=5)

    for idx, splited_file_path in enumerate(splited_file_path_list):
        full_data = []

        for splited_file in splited_file_path :
            full_data += DataLoader.load_pickle_data(file_path=splited_file)

        item_analyzer = ItemAnalyzer()
        unique_category = item_analyzer.get_unique_category(data_set=full_data)
        category_with_count = item_analyzer.get_category_count(data_set=full_data, categories=unique_category,
                                                               filter_num=1000)

        new_data_set = []

        for data in full_data:
            if len(data['image_link']) is 0:
                break

            try:
                category = data['main_category'] + '/' + data['sub_category'] + '/' + data['category_name']

            except:
                category = ''

            for category_string in category_with_count:
                if category == category_string['category'] and len(category) is not 0 :
                    new_data_set.append(data)
                    break

        print("Length of filtered data: " + str(len(new_data_set)))
        print("Num of filtered Categories " + str(len(category_with_count)))

        data_splited_num = 500
        basis = len(new_data_set) // data_splited_num

        print(len(new_data_set))

        formal = 0

        download_file_name = []

        new_save_list = [0]

        for i in range(basis) :
            print("@" * 50)
            print("Downloading Splter-" + str(idx) + " of " + str(len(splited_file_path_list)))
            print("@" * 50)

            splited_data_set = new_data_set[formal:data_splited_num * (i+1)]
            print(str(formal) + ' ~ ' + str(data_splited_num * (i+1)))
            formal = data_splited_num * (i+1)

            image_scraper = NaverImageScraper(data_list=splited_data_set, full_data_length=len(new_data_set))
            new_save_list = image_scraper.get_image(start_index=0, end_index=len(splited_data_set), save_list=new_save_list, process_num=0)
            #image_scraper.multi_get_image(num_of_process=4)

            download_file_name.append(image_scraper.starting_time)

        if len(new_data_set) > formal :
            print("@" * 50)
            print("Downloading Splter-" + str(idx) + " of " + str(len(splited_file_path_list)))
            print("@" * 50)

            splited_data_set = new_data_set[formal:len(new_data_set)]
            print(str(formal) + ' ~ ' + str(len(new_data_set)))

            image_scraper = NaverImageScraper(data_list=splited_data_set, full_data_length=len(new_data_set))
            new_save_list = image_scraper.get_image(start_index=0, end_index=len(splited_data_set), save_list=new_save_list, process_num=0)
            #image_scraper.multi_get_image(num_of_process=4)

            download_file_name.append(image_scraper.starting_time)

        for name in download_file_name :
            print(name)
    '''
    
    '''
    p = DataLoader.load_pickle_data(file_path=settings.ITEM_DATABASE_PATH + 'naver_image_scraper' + '/2020_10_11_15_57/0.pkl')
    print(len(p))
    '''