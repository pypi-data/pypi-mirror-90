from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper import settings


class ErrorFileController:
    def __init__(self, name, date_time):
        self.name = name
        self.date_time = date_time

        self.base_path = settings.ERROR_LOG_DATABASE_PATH + name + '/' + date_time + '/'
        DataLoader.create_if_folder_not_exists(path=self.base_path)

    def init_error_file(self, process_num):
        init_error_list = []

        DataLoader().write_data_in_csv_with_encode_multi(data_list=init_error_list,
                                                         path=self.base_path + str(process_num) + '.csv',
                                                         encoding='utf8')

    def save_error(self, process_num, errors):
        error_log_list = DataLoader.load_data_from_csv_multi_with_encode(file_path=self.base_path + str(process_num) + '.csv',
                                                                         encoding='utf8')
        for e in errors:
            error_log_list.append(e)

        DataLoader().write_data_in_csv_with_encode_multi(data_list=error_log_list,
                                                         path=self.base_path + str(process_num) + '.csv', encoding='utf8')