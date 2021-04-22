from detector import ExtraDetector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging.config

logging.config.fileConfig(fname='logging_config.ini')
logger = logging.getLogger('extra')


class NoExtraTimeException(Exception):
    pass


class NuxChecker:
    extra_events = []
    extra_detector = ExtraDetector()

    def get_extra(self):
        extra_events = self.extra_detector.get_extra()
        empty_sports = []
        for e in extra_events:
            try:
                self.check_sport(e)
            except NoExtraTimeException as e:
                empty_sports.append(str(e))
        if empty_sports:
            logger.debug(f'empty sports: {" ".join(empty_sports)}')

    def check_sport(self, sport):
        if not sport[1]:
            raise NoExtraTimeException(f'{sport[0]}')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
        driver.get(f"https://nuxbet.com/live?sport_id={sport[0]}")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//*[@class='liveMark']"))
            )
        except TimeoutException as e:
            return
        events_elements = driver.find_elements_by_xpath("//div[@class='eventItemWrap']")
        for event in sport[1]:
            try:
                self.check_event_element(events_elements, event)
            except AssertionError:
                ele = driver.find_element_by_xpath('//div[@class="appWrap"]')
                total_height = ele.size["height"]
                driver.set_window_size(1920, total_height)
                driver.save_screenshot(f"./screens/{event[0]}_vs_{event[1]}.png")
                logger.debug(f'saved {event[0]}_vs_{event[1]}')
        driver.close()

    @staticmethod
    def check_event_element(events_elements, event):
        for event_element in events_elements:
            if event[0] in event_element.text and event[1] in event_element.text:
                element = event_element.find_element_by_xpath(".//div[@class='liveTime']")
                time = element.find_elements_by_xpath(".//span")[3].text
                assert '+' in time
