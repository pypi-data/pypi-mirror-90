from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper.utility.error_file_controller import ErrorFileController
from adnar_scraper.utility.selenium_controller import SeleniumController
from adnar_scraper.utility.save_file_controller import SaveFileController
import time

class BackgroundImageScraper:
    def __init__(self, for_transparent):
        self.scraper_name = "background_image_scraper"
        self.kind = "item"

        self.selenium_controller = SeleniumController()
        self.starting_time = DataLoader.create_file_name()
        self.save_file_controller = SaveFileController(name=self.scraper_name, date_time=self.starting_time, kind=self.kind)

        if for_transparent is False:
            self.front_url = "https://www.toptal.com/designers/subtlepatterns/page/"
            self.pages = 1
            self.back_url = "/?fbclid=IwAR1JLnSLYNSAcI7q-vTtV5dtnQXTmxyBSWRdXRYbelDRAZPUYdtg3wIVEt8"

        else:
            self.url = "https://www.transparenttextures.com/"

        self.download_url_list = []

    def scrape_transparent_images(self):
        save_path = self.save_file_controller.base_path

        driver = self.selenium_controller.get_visual_driver(additional_option_list=["download.default_directory=" + save_path])
        driver.get(self.url)

        download_sites = driver.find_elements_by_xpath(xpath='//a[contains(@class, "pattern-link")]')
        print(len(download_sites))

        for download_site in download_sites:
            if download_site.text == 'Create Wallpaper':
                self.download_url_list.append(download_site.get_attribute(name='href'))

        for url in self.download_url_list:
            driver.get(url)
            download_btn = driver.find_element_by_xpath(xpath='//div[contains(@class, "save-transparent-column col-md-6")]/a')

            download_btn.click()



    def scrape_background_images(self):
        save_path = self.save_file_controller.base_path

        driver = self.selenium_controller.get_visual_driver(additional_option_list=["download.default_directory=" + save_path])

        while self.pages <= 55:
            url = self.front_url + str(self.pages) + self.back_url

            driver.get(url)

            a_tag_list = driver.find_elements_by_xpath(xpath='//a[contains(@class, "download")]')

            for a_tag in a_tag_list:
                download_url = a_tag.get_attribute(name="href")
                self.download_url_list.append(download_url)

            self.pages += 1

        for download_url in self.download_url_list:
            driver.get(download_url)

if __name__ == "__main__":
    scraper = BackgroundImageScraper(for_transparent=True)
    scraper.scrape_transparent_images()