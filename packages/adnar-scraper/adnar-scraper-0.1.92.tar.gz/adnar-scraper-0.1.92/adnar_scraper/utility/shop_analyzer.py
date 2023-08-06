import numpy as np
import matplotlib.pyplot as plt
from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper.utility.database_controller import DatabaseController

import regex as re


class ShopAnalyzer:
    def __init__(self):
        pass

    def get_shop_included_with_mall_data(self, shop_graph_data_set, show_item_data_set, mall_info_data_set):
        not_included_shops = dict()

        for shop_name in shop_graph_data_set.keys():
            if shop_name not in show_item_data_set:
                not_included_shops[shop_name] = True

        filtered_mall_info_list = []

        for mall_info in mall_info_data_set:
            if mall_info["name"] in not_included_shops:
                filtered_mall_info_list.append(mall_info)

        return filtered_mall_info_list

    def get_shop_included(self, shop_graph_data_set, show_item_data_set):
        counts = 0

        for shop_name in shop_graph_data_set.keys():
            if shop_name in show_item_data_set:
                counts += 1

        print(f"Gathered shops : {counts}")

    @staticmethod
    def show_shop_count_graph(data_set, grad):
        x_data = []
        y_data = []

        for idx, data in enumerate(data_set):
            if int(re.sub(pattern=',', repl='', string=data['item_count'])) >= 60000:
                continue

            print(idx/len(data_set) * 100)
            is_in_list = False

            for x_idx, x in enumerate(x_data):
                if int(re.sub(pattern=',', repl='', string=data['item_count'])) == x:
                    is_in_list = True
                    y_data[x_idx] += 1
                    break

            if is_in_list is False:
                x_data.append(int(re.sub(pattern=',', repl='', string=data['item_count'])))
                y_data.append(1)

        # filter data
        x_data.reverse()
        y_data.reverse()

        splited_x_data = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        splited_y_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for idx_x, x in enumerate(splited_x_data):
            splited_x_data[idx_x] = int(splited_x_data[idx_x] / grad)

        for idx_x, x in enumerate(x_data):
            if y_data[idx_x] >= 1:
                formal_splited = 0

                if x > splited_x_data[-1]:
                    splited_y_data[-1] += 1

                else:
                    for splited_x_idx, splited_x in enumerate(splited_x_data):
                        if formal_splited <= x <  splited_x:
                            splited_y_data[splited_x_idx] += y_data[idx_x]

                        formal_splited = splited_x


        # Plot data
        print(splited_x_data)
        print(splited_y_data)

        sum_y = 0

        for y in splited_y_data:
            sum_y += y

        print(len(data_set))
        print(sum_y)

        splited_x_data = np.array(splited_x_data)
        splited_y_data = np.array(splited_y_data)

        # Plot Graph
        plt.plot(splited_x_data, splited_y_data, 'ro')
        plt.grid()

        fig = plt.gcf()

        fig.savefig('shop_graph.png')

        #plt.show()


if __name__ == "__main__":
    # x~100
    shop_with_items = DatabaseController(selected_database='item').get_shop_count_data(db_name='shop_detail_scraper')
    shop_with_graphs = DatabaseController(selected_database='local_shop').get_recent_data(db_name='shop_follower_info_scraper')
    mall_infos = DatabaseController(selected_database='local_shop').get_recent_data(db_name='shop_info_scraper')

    analyzer = ShopAnalyzer()

    filtered_mall = analyzer.get_shop_included_with_mall_data(shop_graph_data_set=shop_with_graphs,
                                              show_item_data_set=shop_with_items,
                                              mall_info_data_set=mall_infos)

    print(len(filtered_mall))

