from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper.utility.save_file_controller import SaveFileController
import re


class ShopFilterer:
    def __init__(self):
        self.scraper_name = "shop_filterer"
        self.kind = "local_shop"

        self.starting_time = DataLoader.create_file_name()
        self.save_file_controller = SaveFileController(name=self.scraper_name, date_time=self.starting_time,
                                                       kind=self.kind)

    def analyze_shops(self, shop_data_set, num_of_portions, min_num, max_num,count_step=1000):
        # show num of shops
        print(f"Num of total shop : {len(shop_data_set)}")

        # show item num in each portion
        shop_portion_list = [0] * num_of_portions

        # val to get average of item num in shop
        num_of_all_items = 0

        # val to get data between min num and max num
        num_of_data_between = 0

        for shop_data in shop_data_set:
            # divide shop with item
            num_of_items = int(re.sub(pattern='\,', string=shop_data["num_of_item"], repl=''))
            portion_index = num_of_items // count_step

            if portion_index > num_of_portions - 1:
                portion_index = num_of_portions - 1

            shop_portion_list[portion_index] += 1

            # Get avg of item num
            num_of_all_items += num_of_items

            # Get data between min num and max num
            if min_num <= num_of_items <= max_num:
                num_of_data_between += 1

        average_of_items = num_of_all_items / len(shop_data_set)

        # print analyzed data
        for idx, portion_data in enumerate(shop_portion_list):
            if idx != (num_of_portions - 1):
                print(f"{count_step * idx} <= x < {count_step * (idx + 1)} : {portion_data} == {int(portion_data / len(shop_data_set) * 100)}%")

            else:
                print(f"{count_step * idx} <= x : {portion_data} == {int(portion_data / len(shop_data_set) * 100)}%")

        print("=" * 50)
        print(f"avg : {average_of_items}")
        print(f"{min_num} <= x <= {max_num} : {num_of_data_between} == {int(num_of_data_between / len(shop_data_set) * 100)}%")

    def filter_shops_by_num_of_items(self, shop_data_set, min_num, max_num):
        # Gather shop's that I already scraped items
        shop_owned_with_items = []

        for shop_data in shop_data_set:
            # Get num of item
            num_of_items = int(re.sub(pattern='\,', string=shop_data["num_of_item"], repl=''))

            if min_num <= num_of_items <= max_num:
                shop_owned_with_items.append(shop_data)

        self.save_file_controller.save_with_string_path(string=f"{min_num}_to_{max_num}", data_set=shop_owned_with_items)

    def filter_shops(self, item_data_set, shop_data_set):
        # Gather shop's that I already scraped items
        shop_owned_with_items = dict()

        for item_data in item_data_set:
            if item_data['mall_name'] not in shop_owned_with_items:
                shop_owned_with_items[item_data['mall_name']] = [item_data]

            else:
                pass

if __name__ == "__main__":
    from adnar_scraper.utility.database_controller import DatabaseController

    filterer = ShopFilterer()

    shop_datas = DatabaseController(selected_database='local_shop').get_all_data_in_path(db_name='shop_info_scraper')

    print('-' * 50)

    filterer.analyze_shops(shop_data_set=shop_datas, num_of_portions=10, count_step=100, min_num=20, max_num=300)

    filterer.filter_shops_by_num_of_items(shop_data_set=shop_datas, min_num=20, max_num=300)
