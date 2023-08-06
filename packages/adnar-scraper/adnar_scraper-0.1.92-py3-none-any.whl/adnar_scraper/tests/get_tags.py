if __name__ == "__main__":
    from adnar_scraper.utility.data_loader import DataLoader
    from adnar_scraper.settings import ITEM_DATABASE_PATH
    from operator import itemgetter

    data_set = DataLoader.load_pickle_data(file_path=ITEM_DATABASE_PATH + 'main_gathered_db/main_item_db_ver_4.pkl')

    have_tag_data = 0
    tags = dict()

    for idx, data in enumerate(data_set):
        print("{}%".format(idx/len(data_set)*100))

        if len(data["tag_data"]) != 0:
            have_tag_data += 1

        for tag in data["tag_data"]:
            if tag in tags:
                tags[tag] += 1

            else:
                tags[tag] = 1

    tag_list = []

    for k, v in tags.items():
        tag_list.append([k, v])

    num_of_item = itemgetter(1)
    tag_list = sorted(tag_list, key=num_of_item, reverse=True)

    print("have_tag : {}/{}, {}%, num_of_tag:{}".format(have_tag_data, len(data_set), have_tag_data / len(data_set) * 100, len(tag_list)))
    DataLoader.write_data_in_csv_with_encode_multi(data_list=tag_list, encoding='utf8', path='E:/databases/ver_1/local_database/item_database/tag_datas/tag_items_2020_12_11.csv')
