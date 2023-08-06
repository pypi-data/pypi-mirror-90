from adnar_scraper.utility.database_controller import DatabaseController
from adnar_scraper import settings


class ItemAnalyzer():
    def __init__(self):
        pass

    @staticmethod
    def get_category_count(data_set, categories, filter_num):
        for data in data_set :
            try :
                category = data['main_category'] + '/' + data['sub_category'] + '/' + data['category_name']

            except :
                category = ''

            for category_string in categories :
                if category == category_string['category'] :
                    category_string['count'] += 1

        new_categories = []

        for category in categories :
            if category['count'] >= filter_num :
                new_categories.append(category)

        return new_categories

    @staticmethod
    def get_unique_category(data_set):
        categories = []

        for data in data_set:
            try :
                category = data['main_category'] + '/' + data['sub_category'] + '/' + data['category_name']

            except :
                category = ''

            if len(category) != 0 :
                categories.append(category)

        categories = set(categories)
        categories = sorted(categories)

        category_with_count = []

        for category in categories:
            category_with_count.append({'category':category, 'count':0})

        print("Num of Categories : " + str(len(categories)))

        return category_with_count

    @staticmethod
    def get_tag_data_count(data_set):
        count = 0

        for data in data_set :
            if len(data['tag_data']) != 0:
                count += 1

        print("Item with tag data count : " + str(count))

if __name__ == "__main__" :
    database_controller = DatabaseController(selected_database='item')

    full_data = database_controller.get_all_data_in_path(db_name=settings.ITEM_DATABASE_PATH + 'shop_detail_scraper')

    item_analyzer = ItemAnalyzer()
    unique_category = item_analyzer.get_unique_category(data_set=full_data)
    category_with_count = item_analyzer.get_category_count(data_set=full_data, categories=unique_category, filter_num=1000)

    for k in category_with_count :
        print(k)