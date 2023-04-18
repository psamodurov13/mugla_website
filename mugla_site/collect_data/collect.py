import requests as rq
from loguru import logger
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random as rd
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import re
import pprint
from selenium.webdriver.common.action_chains import ActionChains
from telegram_notifications.tg_notification import notification


headers = {
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"110.0.5481.177"',
    'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.177", "Not A(Brand";v="24.0.0.0", "Google Chrome";v="110.0.5481.177"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"13.2.1"',
    'sec-ch-ua-wow64': '?0',
}

options = Options()
options.add_argument('headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

# driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

options.add_argument(f'user-agent={headers["User-Agent"]}')
# driver.fullscreen_window()


def collect_data(url, city_name):
    notification(f'Старт парсинга - {city_name} / {url}')
    # url = f'https://www.google.com.tr/maps/search/{keyword.replace(" ", "+")}/@{location},13z'
    # response = rq.get(url, headers=headers)
    # logger.info(f'RESPONSE - {response}')
    # soup = bs(response.text, 'html.parser')
    # logger.info(f'SOUP - {soup}')
    # with open('html.html', 'w') as file:
    #     file.write(response.text)
    # driver.get(f'https://www.google.com.tr/maps/search/{keyword.replace(" ", "+")}/@{location},13z')
    driver.get(url)
    # driver.get('https://sweethomedress.ru/')
    time.sleep(5)
    #
    # footer = driver.find_element(By.CSS_SELECTOR, "div.dS8AEf")
    # delta_y = footer.rect['y']
    # ActionChains(driver).scroll_by_amount(0, delta_y).perform()

    # driver.execute_script('window.scrollTo(0, 650);')
    # time.sleep(1)

    SCROLL_PAUSE_TIME = 2
    # Get scroll height
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # logger.info(f'LH - {last_height}')
    #
    # while True:
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #
    #     # Wait to load page
    #     time.sleep(SCROLL_PAUSE_TIME)
    #
    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     logger.info(f'NH - {new_height}')
    #     if new_height == last_height:
    #         break
    #     last_height = new_height
    loaded_companies = driver.find_elements(By.CSS_SELECTOR, 'div.THOPZb')
    all_comp = [(i.find_element(By.CSS_SELECTOR, '.qBF1Pd'), i.find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('href')) for i in loaded_companies]
    logger.info(f'RESULT - {all_comp}')
    # logger.info(f'HlvSq - {driver.find_element(By.CSS_SELECTOR, ".HlvSq")}')
    result = []
    count = 1
    action = ActionChains(driver)
    while True:
        # driver.execute_script("document.getElementsByClassName('m6QErb').scrollTop = document.getElementsByClassName('m6QErb').scrollHeight;")
        time.sleep(rd.randint(1, 4))
        # left_side = driver.find_element(By.CSS_SELECTOR, '.XltNde')
        all_companies = driver.find_elements(By.CSS_SELECTOR, 'div.THOPZb')
        action.move_to_element(all_companies[0])
        action.perform()
        logger.info(f'LENA - {len(all_companies)}')
        # result.extend(all_companies)
        # logger.info(f'LENL - {len(loaded_companies)}')
        try:
            finish = driver.find_element(By.CSS_SELECTOR, ".HlvSq")
            logger.info(f'FIN {finish.text}')
        except Exception:
            finish = False
        if finish:
            # driver.execute_script('arguments[0].scrollIntoView(true);', all_companies[-1])
            # logger.info(f'FINALL - {len(loaded_companies)}')
            all_companies = driver.find_elements(By.CSS_SELECTOR, 'div.THOPZb')
            # result.extend(all_companies)
            logger.info(f'FINAL-RES - {len(all_companies)}')
            break
        else:
        #     # loaded_companies = all_companies[:]
            logger.info(f'Прокрутка')
            driver.execute_script('arguments[0].scrollIntoView(true);', all_companies[-1])
            count += 1
        #     # time.sleep(5)
    time.sleep(2)
    res = {}
    c = 1
    logger.info(f'AC - {all_companies}')
    res = {
        i.find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('href').replace('&hl=tr&', '&hl=ru&'): {}
        for i in all_companies
    }
    for href in res.keys():
        logger.info(f'C - {c}')
        # logger.info(f'A - {href}')
        # href = i.find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('href')
        logger.info(f'H - {href}')
        try:
            driver.get(href)
            time.sleep(1)
            title = driver.find_element(By.CSS_SELECTOR, '.DUwDvf').text
            city = city_name
            try:
                subtitle = driver.find_element(By.CSS_SELECTOR, '.bwoZTb').text
            except NoSuchElementException:
                subtitle = ''
            category = driver.find_element(By.CSS_SELECTOR, 'button[jsaction="pane.rating.category"]').text
            location = re.findall(r'\d{2}\.\d{2,7}', href)
            logger.info(f'LOCATION - {location}')
            try:
                address = driver.find_element(
                    By.CSS_SELECTOR, 'button[data-item-id="address"]'
                ).get_attribute('aria-label').replace('Адрес: ', '')
            except NoSuchElementException:
                address = ''
            try:
                phone = driver.find_element(
                    By.CSS_SELECTOR, 'button[data-tooltip="Скопировать номер"]'
                ).get_attribute('data-item-id').replace('phone:tel:', '')
            except NoSuchElementException:
                phone = ''
            try:
                website = driver.find_element(
                    By.CSS_SELECTOR, 'a[data-tooltip="Перейти на сайт"]').get_attribute('href')
                logger.info(f'WEBSITE {website}')
            except NoSuchElementException:
                website = ''
            try:
                time.sleep(2)
                open_ = driver.find_elements(
                    By.CSS_SELECTOR, '.OqCZI .y0skZc'
                )
                logger.info(f'OPEN_ - {open_}')
                open_hours = {}
                for i in open_:
                    day = i.find_element(By.CSS_SELECTOR, '.HuudEc button').get_attribute('data-value').split(',')[0]
                    logger.info(f'DAY - {day}')
                    # logger.info(f'DAY TEXT - {day.text}')
                    hours = i.find_element(By.CSS_SELECTOR, '.mxowUb').get_attribute('aria-label')
                    logger.info(f'HOURS - {hours}')
                    open_hours[day] = hours
            except NoSuchElementException:
                open_hours = {}
            try:
                tags_ = driver.find_elements(By.CSS_SELECTOR, '.E0DTEd .LTs0Rc')
                tags = []
                for i in tags_:
                    status = i.find_element(By.CSS_SELECTOR, '.TRbhbd').get_attribute('src')
                    if status == 'https://maps.gstatic.com/consumer/images/icons/2x/ic_done_18px.png':
                        tags.append(i.find_element(By.CSS_SELECTOR, 'div[jstcache="72"]').text)
            except NoSuchElementException:
                tags = []
            try:
                photos = driver.find_element(By.CSS_SELECTOR, 'button.ofKBgf[aria-label="Все"]')
                time.sleep(2)
                driver.execute_script('arguments[0].scrollIntoView(true);', photos)
                photos.click()
                time.sleep(5)
                photos_tags = driver.find_elements(By.CSS_SELECTOR, '.Uf0tqf')
                # styles = [i.get_attribute('style') for i in photos_tags]
                photos_urls = []
                for i in photos_tags:
                    try:
                        driver.execute_script('arguments[0].scrollIntoView(true);', i)
                        time.sleep(1)
                        photos_urls.append(re.search(r'url\("(.*?)"\)', i.get_attribute('style')).group(1))
                    except AttributeError:
                        logger.info(f'Photo error - {i}')
                        time.sleep(1)
            except NoSuchElementException:
                photos_urls = []
            res[href] = {'title': title, 'subtitle': subtitle, 'category': category, 'location': location,
                         'address': address, 'phone': phone, 'website': website, 'open_hours': open_hours, 'tags': tags,
                         'photos_urls': photos_urls, 'city': city}
            for k, v in res[href].items():
                logger.info(f'{k} - {v}')
        except Exception:
            logger.error(f'Ошибка сбора данных о компании {href}')
            logger.exception(Exception)
        c += 1
    pprint.pprint(res)
    notification(f'Парсинг компаний выполнен. Всего - {len(res)}')
    return res


if __name__ == '__main__':
    # collect_data('anaokulu marmaris', '36.8611888,28.2643651')
    collect_data('https://www.google.com/maps/search/restaurants+marmaris/@36.8491159,28.2459951,14z',
                 'Мармарис')
    # collect_data('restaurants marmaris', '36.8611888,28.2643651')
    # collect_data('', '')
    logger.info('DONE')