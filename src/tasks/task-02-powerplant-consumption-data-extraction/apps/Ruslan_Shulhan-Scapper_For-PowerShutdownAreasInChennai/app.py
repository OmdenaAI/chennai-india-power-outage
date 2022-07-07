# import packages
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from collections import defaultdict
import pandas as pd


class SeleniumDriver:
    """
    Class of selenium driver.
    """
    def __init__(self, chrome_driver_path="C:\\Program Files\\chromedriver\\chromedriver"):
        """
        Constractor
        :param chrome_driver_path: chrome driver path on your local machine
        """
        self.driver = None
        self.options = None
        self.chrom_driver_path = chrome_driver_path

        if self.set_driver() == False:
            print("\nWarning - driver or options already exist!!!\n")

    def set_driver(self):
        """
        Setting up the chrom driver with all applicable optional details
        :return: bool
        """
        if self.options is None:
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--window-size=1920x1080")
            self.options.add_argument("--ignore-certificate-errors")
            self.options.add_argument("--incognito")
            self.options.add_argument("--headless")

            if self.driver is None:
                if self.chrom_driver_path is None:
                    while self.chrom_driver_path is None:
                        user_input = input("Web driver path: ")
                        if user_input == "":
                            continue
                        self.chrom_driver_path = user_input

                self.driver = webdriver.Chrome(self.chrom_driver_path, chrome_options=self.options)
                if self.driver is not None:
                    self.driver.set_window_size(1920, 1080)
        else:
            return False
        return True


class Scrapper:
    """
    Class represents the object of scrapper and its internal functionality
    """
    def __init__(self):
        """
        Constractor
        """
        self.container = defaultdict(list)
        self.driver_object = SeleniumDriver()

    def get_pages(self, page_url=""):
        """
        Using chrome driver we are getting the page source
        :param page_url: initial page we start with
        :return: list of html page sources
        """
        all_page_sources = []
        page_number = 1

        while page_number != 139:
            self.driver_object.driver.get(page_url + str(page_number))
            time.sleep(0.5)
            if self.driver_object.driver.page_source is not None:
                all_page_sources.append(self.driver_object.driver.page_source)
            page_number += 1

        print("Number of page sources: ", len(all_page_sources))
        return all_page_sources

    def parse_page(self, html_page_sources=[]):
        """
        Parsing page by using beautiful soup package
        :param html_page_sources: list of html sources that were passed by chrome driver using selenium package
        :return: None
        """
        if len(html_page_sources) > 0:
            for html_page_source in html_page_sources:
                soup = BeautifulSoup(html_page_source, features="html.parser")

                if soup is not None:
                    power_shutdown = soup.find_all(attrs={"class": "veg-cointainer"})

                    if power_shutdown is not None:
                        power_shutdown_areas = power_shutdown[0].find_all(attrs={"class": "w"})

                        if (power_shutdown_areas is not None) and (len(power_shutdown_areas) > 0):
                            for power_shutdown_area in power_shutdown_areas:
                                text = power_shutdown_area.find_all(attrs={"class": "cont"})[0]
                                text = text.getText()

                                title = power_shutdown_area.find_all(attrs={"face": "georgia"})[0]
                                title = title.getText()

                                posted_on = power_shutdown_area.find_all(attrs={"class": "read"})[0]
                                posted_on = posted_on.getText()
                                self.parse_text(title_and_text={"title": title, "text": text, "posted_on": posted_on})
        return None

    def parse_text(self, title_and_text):
        """
        Parsing original text into separate categories
        :param title_and_text: dict that holds the elements of html text in term of key/value pairs
        :return: None
        """
        if len(title_and_text) > 0:
            title_original = title_and_text["title"] if "title" in title_and_text.keys() else ""
            text_original = title_and_text["text"] if "text" in title_and_text.keys() else ""
            posted_on_original = title_and_text["posted_on"] if "posted_on" in title_and_text.keys() else ""

            self.container["title_original"].append(self.clean_title(title_original))
            self.container['text_original'].append(text_original)
            self.container['posted_on_original'].append(posted_on_original)

            date_of_power_shutdown = ""
            if title_original != "":
                date_of_power_shutdown = self.get_date_from_title(title_original)
            self.container['date_of_power_shutdown'].append(date_of_power_shutdown)
        return None

    def get_date_from_title(self, text=""):
        """
        Retriving date information from title
        :param text: original text of the title presented as string
        :return: string in the term of the date
        """
        container_for_digits = []
        for char in text:
            if char.isdigit():
                container_for_digits.append(char)

        if len(container_for_digits) == 8:
            day = "".join(container_for_digits[:2])
            month = "".join(container_for_digits[2:4])
            year = "".join(container_for_digits[4:])
            return month + "-" + day + "-" + year
        elif len(container_for_digits) > 0:
            return "".join(container_for_digits)
        else:
            return "n/a"

    def clean_title(self, text=""):
        """
        Cleaning title from irrelevant characters
        :param text: original text in term of the string
        :return: clean text as string
        """
        text = text.replace("\n ", "")
        text = text.replace("\t", "")
        text = text.strip()
        return text

    def scrape_data(self):
        """
        Main method to proceed with scrapping data from the html pages
        :return: None
        """
        start_url = "https://www.livechennai.com/powercut_schedule.asp?KW=&catid=16&orderby=&PN="
        all_html_page_sources = self.get_pages(page_url=start_url)
        self.parse_page(html_page_sources=all_html_page_sources)
        return None

    def save_data(self):
        """
        Saving data into csv file
        :return: None
        """
        df = pd.DataFrame(self.container)
        df.to_csv("out.csv", index=False)
        return None

    def close_driver(self):
        """
        Closing chrome driver
        :return: None
        """
        self.driver_object.driver.quit()
        return None


if __name__ == "__main__":
    obj_scrapper = Scrapper()

    obj_scrapper.scrape_data()
    obj_scrapper.save_data()
    obj_scrapper.close_driver()

    # print(obj_scrapper.container)
