import scrapy
import regex as re
from ..items import DetailInfoScraperItem
import csv
from fake_useragent import UserAgent

from random import randint

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

class InfoSpiderSpider(scrapy.Spider):
    name = 'info_spider'

    def __init__(self):
        ua = UserAgent(
            fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')

        self.user_agent_list = []

        for i in range(10000):
            self.user_agent_list.append(ua.random)

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

        for i in self.category_data_list :
            print(i)

    def is_dead_point(self, num):
        if num <= 200 :
            return False

        else :
            return True

    def start_requests(self):
        for category_data in self.category_data_list:
            page = 1

            while self.is_dead_point(num=page) is False:
                page += 1

                yield scrapy.Request(
                    url=self.front_url + category_data["category_id"] + self.mid_url + str(page) + self.back_url,
                    callback=self.get_items, headers={'User-Agent':{self.user_agent_list[randint(0, 9999)]}},
                    meta={'main_category': category_data["main_category"],
                          'sub_category': category_data["sub_category"],
                          'category': category_data['category_name']})

    def get_items(self, response):
        template = response.xpath('/html/body/div/div/div/div/div/div/ul/div')

        print(len(template))

        for element in template :
            pass
            # Get Detail Info & If there is no detail then "Continue"


            # Get Name

            # Get Image href




        '''
        links = []

        for element in template:
            link_template = element.xpath('descendant::a')

            if len(link_template) >= 1:
                item_link = self.check_link(link_polls=link_template)

                if item_link != None :
                    links.append(item_link)

        links = list(set(links))

        for link in links :
            holder = DetailScraperItem()
            holder["main_category"] = response.meta["main_category"]
            holder["sub_category"] = response.meta["sub_category"]
            holder["category"] = response.meta["category"]
            holder["url"] = link

            yield holder

        print(len(links))
        '''