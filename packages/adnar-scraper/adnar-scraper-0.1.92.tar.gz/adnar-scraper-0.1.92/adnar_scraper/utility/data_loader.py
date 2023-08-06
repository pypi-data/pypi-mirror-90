import hickle
import pickle
import csv
import sys
import os
import time


class DataLoader :
    def __init__(self):
        pass

    @staticmethod
    def create_file_name():
        start_time = time.gmtime(time.time())

        starting_time = str(start_time.tm_year) + '_' + str(start_time.tm_mon) + '_' + str(
            start_time.tm_mday) + '_' + str(start_time.tm_hour) + '_' + str(start_time.tm_min) + str(start_time.tm_sec)

        return starting_time

    @staticmethod
    def create_if_folder_not_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def load_data_from_csv_with_encode(file_path, encoding):
        all_datas = []

        f = open(file_path, 'r', encoding=encoding)
        rdr = csv.reader(f)
        for line in rdr:
            try :
                all_datas.append(line[0])
            except :
                pass
        f.close()

        return all_datas

    @staticmethod
    def write_data_in_csv_with_encode_multi(data_list, path, encoding):
        with open(path, 'w+', newline='', encoding=encoding) as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

            for data in data_list:
                writer.writerow(data)

    @staticmethod
    def write_data_in_csv_with_encode(data_list, path, encoding):
        with open(path, 'w+', newline='', encoding=encoding) as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

            for data in data_list:
                writer.writerow([data])

    @staticmethod
    def load_data_from_csv(file_path):
        all_datas = []

        f = open(file_path, 'r')
        rdr = csv.reader(f)
        for line in rdr:
            try :
                all_datas.append(line[0])
            except :
                pass
        f.close()

        return all_datas

    @staticmethod
    def load_data_from_csv_multi(file_path):
        all_datas = []

        csv.field_size_limit(sys.maxsize)

        f = open(file_path, 'r')
        rdr = csv.reader(f)
        for line in rdr:
            try :
                all_datas.append(line)
            except :
                pass
        f.close()

        return all_datas

    @staticmethod
    def load_data_from_csv_multi_with_encode(file_path, encoding):
        all_datas = []

        f = open(file_path, 'r', encoding=encoding)
        rdr = csv.reader(f)
        for line in rdr:
            try :
                all_datas.append(line)
            except :
                pass
        f.close()

        return all_datas

    @staticmethod
    def write_data_in_csv(data_list, path):
        with open(path, 'w+', newline='', encoding="cp949") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

            for data in data_list:
                writer.writerow([data])

    @staticmethod
    def save_hickle_data(data, file_path):
        print('Hickling data @', file_path)
        # file_handler = open(file_path, "wb")
        hickle.dump(data, file_path + '.hkl', mode='w')
        # pickle.dump(data, file_handler,protocol=4)
        # file_handler.close()

    @staticmethod
    def load_hickle_data(file_path):
        with open(file_path, 'r') as f:
            data = hickle.load(f)

        return data

    @staticmethod
    def save_pickle_data(data, file_path):
        print('Pickling data @', file_path)
        # file_handler = open(file_path, "wb")
        file_handler = open(file_path + '.pkl', "wb")
        pickle.dump(data, file_handler, protocol=4)
        # pickle.dump(data, file_handler,protocol=4)
        file_handler.close()

    @staticmethod
    def load_pickle_data(file_path):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)

        return data
