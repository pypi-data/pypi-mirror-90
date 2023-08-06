import re
from adnar_scraper.settings import SEO_DATABASE_PATH


class CategoryDataCounter:
    def __init__(self, skeleton):
        self.skeleton_dict = self.convert_skeleton_to_dict(skeleton)
        self.file_name = DataLoader.create_file_name()
        self.name = "category_data_counter"

    @staticmethod
    def convert_skeleton_to_dict(skeleton):
        skeleton_dict = dict()

        for category in skeleton:
            category_key = re.sub(pattern="\/", repl="_", string=f"{category[0]}&{category[1]}&{category[2]}")
            skeleton_dict[category_key] = int(category[3])

        return skeleton_dict

    def convert_dict_to_skeleton(self):
        skeleton = []

        for category_key, category_value in self.skeleton_dict.items():
            splited_category = category_key.split("&")
            splited_category += [category_value]

            skeleton.append(splited_category)

        return skeleton

    def save_skeleton(self, skeleton):
        DataLoader.write_data_in_csv_with_encode_multi(data_list=skeleton,
                                                       path=f"{SEO_DATABASE_PATH}{self.name}/lists/{self.file_name}.csv",
                                                       encoding='utf8')

    def count_and_sum_to_skeleton(self, data_set):
        pass

if __name__ == "__main__":
    from adnar_scraper.utility.data_loader import DataLoader

    k = DataLoader.load_data_from_csv_multi_with_encode(file_path='E:/databases/ver_1/local_database/seo_info_database/category_data_counter/category_skeleton.csv',
                                                        encoding='utf8')

    cdc = CategoryDataCounter(skeleton=k)

    import os

    top = "E:/databases/ver_1/local_database/item_database/separated_category_items"

    folder_list = []

    for root, dirs, files in os.walk(top, topdown=False):
        for name in dirs:
            folder_list.append({'path': os.path.join(root, name), 'files': None})

    for folder in folder_list:
        folder['files'] = [x[-1] for x in os.walk(folder['path'])][0]

    # Load all & Integrate data
    for folder in folder_list:
        for file_name in folder['files']:
            print('Data Loaded from "' + folder['path'] + '/' + file_name + '"')
            item = DataLoader.load_pickle_data(file_path=folder['path'] + '/' + file_name)
            print(len(item))

            file_name = re.sub(pattern='\.pkl', repl='', string=file_name)

            cdc.skeleton_dict[file_name] += len(item)

    skeleton_csv = cdc.convert_dict_to_skeleton()
    cdc.save_skeleton(skeleton=skeleton_csv)


