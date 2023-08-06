from adnar_scraper.utility.database_controller import DatabaseController
from adnar_scraper.utility.data_loader import DataLoader


k = DatabaseController(selected_database="local_title")
data = k.get_all_data_in_path(db_name='magazine_scraper')

data = k.get_unique_json_data_set(data_set=data)

save_list = []
save_num = 0

for idx, a in enumerate(data):
    if len(save_list) == 2000:
        DataLoader().write_data_in_csv_with_encode(path='/home/discoverious/Documents/local_database/title_database/split_adjust/titles_ver_1_split_{}.csv'.format(save_num), encoding='utf8', data_list=save_list)
        save_num += 1
        save_list = []

    save_list.append(a['title'])
    save_list.append(a['title'])

print("Count : {}".format(len(data)))

