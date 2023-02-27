import requests as rq
from loguru import logger
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

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
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
options.add_argument(f'user-agent={headers["User-Agent"]}')




def collect_data(keyword, location):
    # url = f'https://www.google.com.tr/maps/search/{keyword.replace(" ", "+")}/@{location},13z'
    # response = rq.get(url, headers=headers)
    # logger.info(f'RESPONSE - {response}')
    # soup = bs(response.text, 'html.parser')
    # logger.info(f'SOUP - {soup}')
    # with open('html.html', 'w') as file:
    #     file.write(response.text)
    driver.get(f'https://www.google.com.tr/maps/search/{keyword.replace(" ", "+")}/@{location},13z')
    # driver.get('https://sweethomedress.ru/')
    time.sleep(3)
    #
    # footer = driver.find_element(By.CSS_SELECTOR, "div.dS8AEf")
    # delta_y = footer.rect['y']
    # ActionChains(driver).scroll_by_amount(0, delta_y).perform()

    driver.execute_script('window.scrollTo(0, 650);')
    time.sleep(2)

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
    loaded_companies = driver.find_elements(By.CSS_SELECTOR, 'div.bfdHYd')
    while True:
        driver.execute_script('arguments[0].scrollIntoView(true);', loaded_companies[-1])
        all_companies = driver.find_elements(By.CSS_SELECTOR, 'div.bfdHYd')
        logger.info(f'LENL - {len(loaded_companies)}')
        logger.info(f'LENA - {len(all_companies)}')
        if len(all_companies) == len(loaded_companies):
            logger.info(f'FINALL - {len(loaded_companies)}')
            logger.info(f'FINALA - {len(all_companies)}')
            break
        else:
            loaded_companies = all_companies[:]
            time.sleep(1)



if __name__ == '__main__':
    collect_data('anaokulu marmaris', '36.8611888,28.2643651')
    # collect_data('', '')
    logger.info('DONE')