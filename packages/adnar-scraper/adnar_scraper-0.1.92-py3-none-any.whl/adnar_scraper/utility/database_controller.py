from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper import settings
import os
import json
import re


class DatabaseController:
    def __init__(self, selected_database):
        if selected_database is 'item':
            self.base_path = settings.ITEM_DATABASE_PATH

        elif selected_database is 'shop':
            self.base_path = settings.SHOP_DATABASE_PATH

        elif selected_database is 'processed_data':
            self.base_path = settings.PROCESSED_DATA_DATABASE_PATH

        elif selected_database is 'image_creator':
            self.base_path = settings.IMAGE_DATA_DATABASE_PATH

        elif selected_database is 'seo_information':
            self.base_path = settings.SEO_DATABASE_PATH

        elif selected_database is 'local_title':
            self.base_path = '/home/discoverious/Documents/local_database/title_database/'

        elif selected_database is 'local_shop':
            self.base_path = '/home/discoverious/Documents/local_database/shop_database/'

        print('-')
        print(self.base_path)

    @staticmethod
    def view_data_set(data_set):
        for data in data_set:
            print(data)

    @staticmethod
    def get_merged_data_set(data_set_list):
        merged_data_set = []

        for data_set in data_set_list:
            merged_data_set += data_set

        return merged_data_set

    @staticmethod
    def filter_useless_items(data_set):
        while True:
            useless_item_found = False
            del_index = 0

            for idx, item in enumerate(data_set):
                if item is ['item_name', 'info_list', 'image_link', 'main_category', 'sub_category', 'category_name']:
                    useless_item_found = True
                    del_index = idx
                    break

            del data_set[del_index]

            if useless_item_found is False:
                break

        return data_set

    @staticmethod
    def get_unique_json_data_set(data_set):
        str_data_set = []

        for data in data_set:
            str_data_set.append(json.dumps(data))

        str_data_set = set(str_data_set)

        filtered_data_list = []

        for data in str_data_set:
            filtered_data_list.append(json.loads(data))

        return filtered_data_list


    def get_splited_data_path(self, db_name, split_rank):
        top = self.base_path + db_name

        folder_list = []

        for root, dirs, files in os.walk(top, topdown=False):
            for name in dirs:
                folder_list.append({'path': os.path.join(root, name), 'files': None})

        for folder in folder_list:
            folder['files'] = [x[-1] for x in os.walk(folder['path'])][0]

        # Get all path & size
        sum_size = 0

        all_file_path = []
        for folder in folder_list:
            for file_name in folder['files']:
                file_size = os.path.getsize(folder['path'] + '/' + file_name)
                sum_size += file_size

                all_file_path.append({'file_path':folder['path'] + '/' + file_name, 'file_size':file_size})

        # Split by file size
        each_split_rank = sum_size // split_rank

        splited_file_path_list = []

        splited_file_path = []
        splited_file_size = 0

        for idx, file_data in enumerate(all_file_path):
            if splited_file_size <= each_split_rank:
                splited_file_size += file_data['file_size']
                splited_file_path.append(file_data['file_path'])

                if idx is len(all_file_path)-1 :
                    splited_file_path_list.append(splited_file_path)

            else :
                splited_file_path_list.append(splited_file_path)

                splited_file_path = [file_data['file_path']]
                splited_file_size = file_data['file_size']

        return splited_file_path_list

    def get_all_data_in_path(self, db_name):
        top = self.base_path + db_name

        folder_list = []

        for root, dirs, files in os.walk(top, topdown=False):
            for name in dirs:
                folder_list.append({'path': os.path.join(root, name), 'files': None})

        for folder in folder_list:
            folder['files'] = [x[-1] for x in os.walk(folder['path'])][0]

        # Load all & Integrate data
        all_data = []

        for folder in folder_list:
            for file_name in folder['files']:
                try :
                    print('Data Loaded from "' + folder['path'] + '/' + file_name + '"')
                    all_data += DataLoader.load_pickle_data(file_path=folder['path'] + '/' + file_name)

                except Exception as e :
                    print(e)

        print('All data Length: ' + str(len(all_data)))

        return all_data

    def get_category_datas_in_path(self, db_name, process_num_list):
        full_cat = []

        for process_num in process_num_list:
            top = self.base_path + db_name

            folder_list = []

            for root, dirs, files in os.walk(top, topdown=False):
                for name in dirs:
                    folder_list.append({'path': os.path.join(root, name), 'files': None})

            for folder in folder_list:
                folder['files'] = [x[-1] for x in os.walk(folder['path'])][0]

            # Load all & Integrate data
            tag_list = {'process_num': process_num, 'item_list': []}

            for folder in folder_list:
                for file_name in folder['files']:
                    try:
                        print('Data Loaded from "' + folder['path'] + '/' + file_name + '"')

                        if re.search(string=folder['path'], pattern='process_{}'.format(process_num)) is not None:
                            data_set = DataLoader.load_pickle_data(file_path=folder['path'] + '/' + file_name)

                            for data in data_set:
                                try:
                                    price = data["item_price"]

                                    if price is not None:
                                        tag_list['item_list'].append({'main_category':data['main_category'], 'sub_category': data['sub_category'], 'category_name': data['category_name']})

                                except Exception as e:
                                    pass

                    except Exception as e:
                        print(e)

            tag_list['item_list'] = self.get_unique_json_data_set(data_set=tag_list['item_list'])
            full_cat.append(tag_list)
            print('Process - {} : All data Length: {}'.format(process_num, len(tag_list['item_list'])))

        return full_cat

    def get_tag_datas_in_path(self, db_name):
        top = self.base_path + db_name

        folder_list = []

        for root, dirs, files in os.walk(top, topdown=False):
            for name in dirs:
                folder_list.append({'path': os.path.join(root, name), 'files': None})

        for folder in folder_list:
            folder['files'] = [x[-1] for x in os.walk(folder['path'])][0]

        # Load all & Integrate data
        tag_list = []

        for folder in folder_list:
            for file_name in folder['files']:
                try:
                    print('Data Loaded from "' + folder['path'] + '/' + file_name + '"')
                    data_set = DataLoader.load_pickle_data(file_path=folder['path'] + '/' + file_name)

                    for data in data_set:
                        try:
                            price = data["item_price"]

                            if price is not None:
                                tag_list.append(data["tag_data"])

                        except Exception as e:
                            pass

                except Exception as e:
                    print(e)

        tag_list = self.get_unique_json_data_set(data_set=tag_list)

        print('All data Length: ' + str(len(tag_list)))

        return tag_list

    def get_shop_count_data(self, db_name):
        top = self.base_path + db_name

        folder_list = []

        for root, dirs, files in os.walk(top, topdown=False):
            for name in dirs:
                folder_list.append({'path': os.path.join(root, name), 'files': None})

        for folder in folder_list:
            folder['files'] = [x[-1] for x in os.walk(folder['path'])][0]

        # Load all & Integrate data
        mall_dict = dict()

        for folder in folder_list:
            for file_name in folder['files']:
                try:
                    print('Data Loaded from "' + folder['path'] + '/' + file_name + '"')
                    data_set = DataLoader.load_pickle_data(file_path=folder['path'] + '/' + file_name)

                    for data in data_set:
                        try:
                            price = data["item_price"]

                            if price is not None:
                                if data["mall_name"] not in mall_dict:
                                    mall_dict[data["mall_name"]] = 1

                                else:
                                    mall_dict[data["mall_name"]] += 1

                        except Exception as e:
                            pass

                except Exception as e:
                    print(e)

        print('All data Length: ' + str(len(mall_dict)))

        return mall_dict


    def get_mall_name_in_path(self, db_name):
        top = self.base_path + db_name

        folder_list = []

        for root, dirs, files in os.walk(top, topdown=False):
            for name in dirs:
                folder_list.append({'path': os.path.join(root, name), 'files': None})

        for folder in folder_list:
            folder['files'] = [x[-1] for x in os.walk(folder['path'])][0]

        # Load all & Integrate data
        mall_names = []

        for folder in folder_list:
            for file_name in folder['files']:
                try:
                    print('Data Loaded from "' + folder['path'] + '/' + file_name + '"')
                    data_set = DataLoader.load_pickle_data(file_path=folder['path'] + '/' + file_name)

                    for data in data_set:
                        try:
                            price = data["item_price"]

                            if price is not None:
                                mall_names.append(data["mall_name"])

                        except Exception as e:
                            pass

                except Exception as e:
                    print(e)

        mall_names = set(mall_names)

        print('All data Length: ' + str(len(mall_names)))

        return mall_names

    def get_recent_data(self, db_name):
        top = self.base_path + db_name

        folder_list = []

        for root, dirs, files in os.walk(top, topdown=False):
            for name in dirs:
                folder_list.append({'path': os.path.join(root, name), 'files': None})

        for folder in folder_list:
            folder['files'] = [x[-1] for x in os.walk(folder['path'])][0]

        # get times
        recent_time_data = {'time_data': 0, 'path': None}

        for folder in folder_list:
            for file_name in folder['files']:
                try:
                    time_stamp = folder['path'].split('/')[-1].split('_')

                    year_to_second = 60 * 60 * 24 * 30 * 12 * int(time_stamp[0])
                    month_to_second = 60 * 60 * 24 * 30 * int(time_stamp[1])
                    day_to_second = 60 * 60 * 24 * int(time_stamp[2])
                    hour_to_second = 60 * 60 * int(time_stamp[3])

                    time_data = year_to_second + month_to_second + day_to_second + hour_to_second + int(time_stamp[-1])

                    if time_data > recent_time_data['time_data']:
                        recent_time_data['time_data'] = time_data
                        recent_time_data['path'] = folder['path'] + '/' + file_name

                except Exception as e:
                    print(e)

        recent_data = DataLoader.load_pickle_data(file_path=recent_time_data['path'])

        print(f"Data loaded from {recent_time_data['path']}")
        print('All data Length: ' + str(len(recent_data)))

        return recent_data

    def get_tag_with_category_attribute(self, db_name):
        base_path = settings.UTILITY_DATABASE_PATH + 'attribute_information/'

        with open(base_path + "attribute_ver_2.json") as json_file:
            category_information = json.load(json_file)['items']

        top = self.base_path + db_name

        folder_list = []

        for root, dirs, files in os.walk(top, topdown=False):
            for name in dirs:
                folder_list.append({'path': os.path.join(root, name), 'files': None})

        for folder in folder_list:
            folder['files'] = [x[-1] for x in os.walk(folder['path'])][0]

        # Load all & Integrate data
        item_list = []
        file_num = 1
        num_of_item = 0

        for idx, folder in enumerate(folder_list):
            for file_name in folder['files']:
                try:
                    print('Load percent : {}'.format(idx/len(folder_list) * 100))
                    print('Data Loaded from "' + folder['path'] + '/' + file_name + '"')
                    data_set = DataLoader.load_pickle_data(file_path=folder['path'] + '/' + file_name)

                    for data in data_set:
                        try:
                            category_attribute = None

                            for category in category_information:
                                if category['prime_category'] == data['main_category'] and category['sub_category'] ==  data['sub_category'] \
                                        and category['category'] == data['category_name']:
                                    category_attribute = category['attribute']

                            if category_attribute is not None:
                                if len(category_attribute) == len(data['info_list']):
                                    length_of_attr = 0

                                    for each_category_attribute in category_attribute:
                                        exist_in = False

                                        for each_data_attribute in data['info_list']:
                                            if each_category_attribute == list(each_data_attribute.keys())[0]:
                                                exist_in = True
                                                break

                                        if exist_in is True:
                                            length_of_attr += 1

                                    if length_of_attr == len(category_attribute):
                                        item_list.append(data)
                                        num_of_item += 1

                        except Exception as e:
                            pass

                    print('Current length of item_list : {}'.format(num_of_item))

                    if len(item_list) >= 100000:
                        DataLoader.save_pickle_data(data=item_list,
                                                    file_path=settings.ITEM_DATABASE_PATH + 'tag_datas/tag_with_category_ver_{}'.format(file_num))

                        file_num += 1
                        item_list = []

                except Exception as e:
                    print(e)

        item_list = self.get_unique_json_data_set(data_set=item_list)

        print('All data Length: ' + str(len(item_list)))

        return item_list

if __name__ == "__main__":
    ctn = DatabaseController(selected_database='local_shop')
    ctn.get_recent_data('shop_filterer')

