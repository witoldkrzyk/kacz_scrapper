from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from app.models import Source, Tins
from datetime import datetime


class KaczmarskiSelenium:
    def __init__(self, tin):
        self.url = 'https://kaczmarski.pl/gielda-wierzytelnosci'
        self.start_date = None
        self.end_date = None
        self.driver = None
        self.tin = tin

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--window-size=1600,900')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def tin_obj(self):
        tin, _ = Tins.objects.get_or_create(tin=self.tin)
        return tin

    def find_elem_within_seconds_for_element(self, by, value, duration=0):
        time.sleep(duration)
        try:
            return self.driver.find_element(by, value)
        # At the moment, I do not know all the possible exceptions on this page
        except:
            return None

    def close_startup_popout(self):
        elem = self.find_elem_within_seconds_for_element(By.CLASS_NAME, 'wh-popUp-close', 3)
        if elem:
            try:
                elem.click()
            # At the moment, I do not know all the possible exceptions on this page
            except:
                raise Exception("cannot to close startup popout")

    def input_tin(self):
        input_elem = self.find_elem_within_seconds_for_element(By.XPATH, '/html/body/form/div[5]/div/div/main/div/section/div/form/div[1]/div[2]/div[1]/div[2]/div[1]/input', 4)
        if input_elem:
            try:
                input_elem.send_keys(self.tin)
            # At the moment, I do not know all the possible exceptions on this page
            except:
                raise Exception(f"cannot to send keys with tin number into input, tin: {self.tin}")

    def click_search_btn(self):
        search_btn_elem = self.find_elem_within_seconds_for_element(By.CLASS_NAME, 'ki-market-searcher-button', 4)
        if search_btn_elem:
            try:
                search_btn_elem.click()
            # At the moment, I do not know all the possible exceptions on this page
            except:
                raise Exception("cannot to click search button")

    def click_for_more_info(self):
        more_info_elem = self.find_elem_within_seconds_for_element(By.XPATH,
                                                                   '/html/body/form/div[5]/div/div/main/div/section/div/form/div[2]/div/div[2]/div[1]',
                                                                   3)
        if more_info_elem:
            try:
                more_info_elem.click()
            # At the moment, I do not know all the possible exceptions on this page
            except:
                raise Exception("cannot to click more info button")

    def get_content_from_url(self):
        self.driver.get(self.url)
        self.close_startup_popout()
        self.input_tin()
        self.click_search_btn()
        self.click_for_more_info()

    def name_of_company(self):
        elem = self.find_elem_within_seconds_for_element(By.XPATH,
                                                         '/html/body/form/div[5]/div/div/main/div/section/div/form/div[2]/div/div[2]/div[1]/div[1]')
        return elem.text.replace('DŁUŻNIK\n', '') if elem else elem

    def nip_number(self):
        elem = self.find_elem_within_seconds_for_element(By.XPATH,
                                                         '/html/body/form/div[5]/div/div/main/div/section/div/form/div[2]/div/div[2]/div[1]/div[2]').text.replace(
            'NIP\n', '')
        return elem.text.replace('NIP\n', '') if elem else elem

    def amount_price(self):
        elem = self.find_elem_within_seconds_for_element(By.XPATH,
                                                         '/html/body/form/div[5]/div/div/main/div/section/div/form/div[2]/div/div[2]/div[1]/div[3]')

        return elem.text.replace('KWOTA ZADŁUŻENIA\n', '') if elem else elem

    def company_address(self):
        elem = self.find_elem_within_seconds_for_element(By.XPATH,
                                                         '/html/body/form/div[5]/div/div/main/div/section/div/form/div[2]/div/div[2]/div[2]/div[1]/div[1]')

        return elem.text.replace('ADRES\n', '') if elem else elem

    def document_type(self):
        elem = self.find_elem_within_seconds_for_element(By.XPATH,
                                                         '/html/body/form/div[5]/div/div/main/div/section/div/form/div[2]/div/div[2]/div[2]/div[1]/div[2]')

        return elem.text.replace('RODZAJ/TYP DOKUMENTU STANOWIĄCY PODSTAWĘ DLA WIERZYTELNOŚCI\n', '') if elem else elem

    def number_id(self):
        elem = self.find_elem_within_seconds_for_element(By.XPATH,
                                                         '/html/body/form/div[5]/div/div/main/div/section/div/form/div[2]/div/div[2]/div[2]/div[1]/div[4]')

        return elem.text.replace('NUMER\n', '') if elem else elem

    def price(self):
        elem = self.find_elem_within_seconds_for_element(By.XPATH,
                                                         '/html/body/form/div[5]/div/div/main/div/section/div/form/div[2]/div/div[2]/div[2]/div[2]/div')

        return elem.text.replace('CENA ZADŁUŻENIA\n', '') if elem else elem

    def save_source(self):
        if self.name_of_company():
            Source(
                tin=self.tin_obj(),
                company_name=self.name_of_company(),
                total_amount=self.amount_price(),
                company_address=self.company_address(),
                document_type=self.document_type(),
                number_id=self.number_id(),
                sell_for=self.price(),
                is_exists=True,
                start_ts=datetime.fromtimestamp(self.start_date),
                parsing_ts=datetime.fromtimestamp(self.end_date - self.start_date)
            ).save()
        else:
            Source(
                tin=self.tin_obj(),
                start_ts=datetime.fromtimestamp(self.start_date),
                parsing_ts=datetime.fromtimestamp(self.end_date - self.start_date)
            ).save()


        self.tin_obj().updated_at = datetime.now()
        self.tin_obj().save()

    def run(self):
        try:
            self.init_driver()
            self.start_date = time.time()
            self.get_content_from_url()
            self.end_date = time.time()
            self.save_source()
        except Exception as e:
            print(e)
        self.driver.quit()
