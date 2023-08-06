import scrapy
import regex as re
#from preprocessor.data_loader import DataLoader
from ..items import DetailScraperItem
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

class DetailSpiderSpider(scrapy.Spider):
    name = 'detail_spider'

    def __init__(self) :



        absolute_path = 'C:/Users/강시우/Desktop/seo_scraper/'

        self.front_url = "https://msearch.shopping.naver.com/search/category?sort=rel&pagingIndex="
        self.middle_url = "&pagingSize=40&viewType=lst&productSet=soho&catId="
        self.back_url = "&frm=NVSHSHO&selectedFilterTab=seller"

        loaded_category = DataLoader().load_data_from_csv_multi_with_encode(filepath=absolute_path + 'database/all_category.csv', encoding='utf8')

        self.category_data_list = []

        for category_data in loaded_category :
            self.category_data_list.append(
                {"main_category": category_data[0],
                 "sub_category": category_data[1],
                 "category_name": category_data[2],
                 "category_id": category_data[3]})

    def is_dead_point(self, num):
        if num <= 200 :
            return False

        else :
            return True

    def check_link(self, link_polls):
        for link_poll in link_polls :
            extracted_link = link_poll.xpath('@href').extract_first()

            if re.match(pattern="https://cr.shopping.naver.com/adcr.nhn?", string=extracted_link) != None :
                return extracted_link

    def create_headers(self, num):
        return {'User-Agent': 'this_is_mine' + str(num)}

    def start_requests(self):
        for category_data in self.category_data_list :
            page = 1

            print(self.front_url + str(1) + self.middle_url + category_data["category_id"] + self.back_url)

            while self.is_dead_point(num=page) is False :
                page += 1

                yield scrapy.Request(
                       url=self.front_url + str(page) + self.middle_url + category_data["category_id"] + self.back_url,
                       callback=self.get_items, headers=self.create_headers(num=page),
                       meta={'main_category': category_data["main_category"], 'sub_category': category_data["sub_category"],
                             'category': category_data['category_name']})

    def get_items(self, response):
        template = response.xpath('/html/body/div/div/div/div/ul/li')

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
