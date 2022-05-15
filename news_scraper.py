import time
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd


def get_us_stock_news(stock, p_num=70):
    # Scraping News Headlines from Investing.com
    base_url = 'https://www.investing.com/'

    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url=base_url)
    driver.maximize_window()

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="PromoteSignUpPopUp"]/div[2]/i')))
    time.sleep(40)
    popup_close_button = driver.find_element_by_xpath('//*[@id="PromoteSignUpPopUp"]/div[2]/i')
    popup_close_button.click()

    search_box = driver.find_element_by_xpath('/html/body/div[5]/header/div[1]/div/div[3]/div[1]/input')
    search_box.send_keys(stock)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)

    search_result = driver.find_element_by_xpath('//*[@id="fullColumn"]/div/div[2]/div[2]/div[1]/a[1]')
    search_result.click()
    time.sleep(3)

    current_url = driver.current_url
    news_url = current_url + "-news"

    driver.get(news_url)

    headlines = list()
    for page_num in range(2, p_num):
        for list_num in range(1, 11):
            headline = driver.find_element_by_xpath('//*[@id="leftColumn"]/div[8]/article[' + str(list_num) + ']/div[1]/a').text
            headlines.append(headline)
        next_url = news_url + "/" + str(page_num)
        driver.get(next_url)

    headline_df = pd.DataFrame(headlines)

    headline_df.to_csv('C:/Users/nanal/Desktop/데이터 모음/Stocks/{}_headlines.csv'.format(stock),
                   encoding='utf-8')
