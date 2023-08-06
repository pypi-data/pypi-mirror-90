from adnar_scraper import settings

from adnar_scraper.utility.data_loader import DataLoader


class SaveFileController:
    def __init__(self, name, date_time, kind):
        self.name = name
        self.date_time = date_time

        folder_path = None

        if kind is 'shop':
            folder_path = settings.SHOP_DATABASE_PATH

        elif kind is 'item':
            folder_path = settings.ITEM_DATABASE_PATH

        elif kind is 'processed_data':
            folder_path = settings.PROCESSED_DATA_DATABASE_PATH

        elif kind is 'image_creator':
            folder_path = settings.IMAGE_DATA_DATABASE_PATH

        elif kind is 'seo_information':
            folder_path = settings.SEO_DATABASE_PATH

        elif kind is 'local_title':
            folder_path = '/home/discoverious/Documents/local_database/title_database/'

        elif kind is 'local_shop':
            folder_path = '/home/discoverious/Documents/local_database/shop_database/'

        self.base_path = folder_path + name + '/' + date_time + '/'
        DataLoader.create_if_folder_not_exists(path=self.base_path)

        self.saving_version = 0

    def save_train_data(self, x_data_list, image_x_data_list, y_data_list, classifier, prime_category=None, sub_category=None, category=None):
        print("=" * 50)
        print('Train data(X,Image_X,Y) saved')

        if classifier is 'category':
            category_path = 'category' + '/'

            DataLoader.create_if_folder_not_exists(path=self.base_path + category_path)

            DataLoader.save_pickle_data(data=x_data_list, file_path=self.base_path + category_path + 'x_data')
            DataLoader.save_pickle_data(data=image_x_data_list, file_path=self.base_path + category_path + 'image_x_data')
            DataLoader.save_pickle_data(data=y_data_list, file_path=self.base_path + category_path + 'y_data')

        elif classifier is 'attribute':
            attribute_path = 'attribute' + '/' + prime_category + '/' + sub_category + '/' + category + '/'

            DataLoader.create_if_folder_not_exists(path=self.base_path + attribute_path)

            DataLoader.save_pickle_data(data=x_data_list, file_path=self.base_path + attribute_path + 'x_data')
            DataLoader.save_pickle_data(data=image_x_data_list, file_path=self.base_path + attribute_path + 'image_x_data')
            DataLoader.save_pickle_data(data=y_data_list, file_path=self.base_path + attribute_path + 'y_data')

    def save_text_vec_model(self, vectorizer, features):
        print("=" * 50)
        print('Text vectorizer & feature saved')

        DataLoader.save_pickle_data(data=vectorizer, file_path=self.base_path + 'text_vectorizer')
        DataLoader.save_pickle_data(data=features, file_path=self.base_path + 'text_features')

    def save_with_string_path(self, string, data_set):
        print("=" * 50)

        absolute_path = self.base_path + string
        print('{} : saved {} data'.format(string, len(data_set)))

        DataLoader.save_pickle_data(data=data_set, file_path=absolute_path)
        print("=" * 50)

    def save_with_namespace(self, namespace, data_set):
        saving_time = DataLoader.create_file_name()

        print("=" * 50)

        DataLoader.create_if_folder_not_exists(path=self.base_path + namespace + '/')

        absolute_path = self.base_path + namespace + '/' + saving_time

        print('{} : saved {} data'.format(namespace, len(data_set)))

        DataLoader.save_pickle_data(data=data_set, file_path=absolute_path)
        print("=" * 50)

    def save_data_memory_saving_version(self, process_num, data_set):
        saving_time = DataLoader.create_file_name()

        print("=" * 50)

        DataLoader.create_if_folder_not_exists(path=self.base_path + 'process_{}/'.format(process_num))

        absolute_path = self.base_path + 'process_{}/'.format(process_num) + saving_time

        print('Process_' + str(process_num) + ' : saved ' + str(len(data_set)) + ' data')

        DataLoader.save_pickle_data(data=data_set, file_path=absolute_path)
        print("=" * 50)

    def save_data_memory_with_out_process(self, data_set):
        saving_time = DataLoader.create_file_name()

        print("=" * 50)

        DataLoader.create_if_folder_not_exists(path=self.base_path)
        absolute_path = self.base_path + saving_time

        print('saved ' + str(len(data_set)) + ' data')

        DataLoader.save_pickle_data(data=data_set, file_path=absolute_path)
        print("=" * 50)

    def save_data_each(self, process_num, data_set):
        print("=" * 50)
        absolute_path = self.base_path + str(process_num)

        data_list = []

        try:
            data_list = DataLoader.load_pickle_data(file_path=absolute_path + '.pkl')

        except OSError as e:
            print(e)
            if e.errno is 2:
                data_list = []

        print('Process_' + str(process_num) + ' : loaded ' + str(len(data_list)) + ' data')

        for item in data_set:
            data_list.append(item)

        print('Process_' + str(process_num) + ' : saved ' + str(len(data_list)) + ' data')

        DataLoader.save_pickle_data(data=data_list, file_path=absolute_path)
        print("=" * 50)