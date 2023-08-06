# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exporters import JsonItemExporter, CsvItemExporter
#from preprocessor.data_loader import DataLoader
import time
import csv

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

class DetailScraperPipeline:
    def process_item(self, item, spider):
        print(item)
        return item

class CsvPipeline(object):
    def __init__(self):
        self.absolute_path = 'C:/users/강시우/desktop/seo_scraper/'

        current_time = time.gmtime(time.time())

        dummy_item = []
        self.file_name = str(current_time.tm_year) + '_' +  str(current_time.tm_mon) + '_' +  str(current_time.tm_mday) + '_' + str(current_time.tm_hour) + '_' + str(current_time.tm_min) + '.csv'

        DataLoader().write_data_in_csv_with_encode_multi(data_list=dummy_item, path=self.absolute_path + 'database/base/all_items/' + self.file_name, encoding='utf8')

        dummy_file = DataLoader().load_data_from_csv_multi_with_encode(filepath=self.absolute_path + 'database/base/all_items/' + self.file_name, encoding='utf8')
        self.dummy_file_start_length = len(dummy_file)

        self.file = open(self.absolute_path + 'database/base/all_items/' + self.file_name, 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf8')
        self.exporter.start_exporting()

        self.start = time.time()

    def close_spider(self, spider):
        '''
        1. Scraper 주기, 페이지 수, Internal delay, running_time
        2. Scraper 주기에 따른 data 추가 개수(40으로 나눠서 추가된 page) - 주기를 늘리거나, 페이지수를 줄여야하기 때문에, 혹은 internal_delay를 조정해줘야해서
        2. Deleter 주기
        3. Deleter 주기에 따른 data 삭제 개수(40으로 나눠서 삭제된 page) - 주기를 늘려야할 수 있기 때문에

        '''
        #
        dummy_file = DataLoader().load_data_from_csv_multi_with_encode(
            filepath=self.absolute_path + 'database/base/all_items/' + self.file_name, encoding='utf8')
        dummy_file_end_length = len(dummy_file)

        appended_length = dummy_file_end_length - self.dummy_file_start_length
        appended_page = appended_length // 40
        scraper_cycle = 6
        internal_delay = 10
        total_running_time = int(time.time() - self.start)

        scraper_setting_file = DataLoader().load_data_from_csv_multi_with_encode(
            filepath=self.absolute_path + 'database/scheduler_settings/for_scraper/ver_1.csv', encoding='utf8')
        scraper_setting_file.append([appended_length, appended_page, scraper_cycle, internal_delay, total_running_time])

        DataLoader().write_data_in_csv_with_encode_multi(data_list=scraper_setting_file,
                                                         path=self.absolute_path + 'database/scheduler_settings/for_scraper/ver_1.csv',
                                                         encoding='utf8')

        self.exporter.finish_exporting()
        self.file.close()



    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item