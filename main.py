from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from string import Template
import time
import random
import os
import re
import json
import yaml
from typing import Union

def get_configs():
    """retrieves the settings and breakpoint from the settings file"""
    global configs
    with open('config.yaml', 'r') as f:
        configs = yaml.safe_load(f)
        print(configs)



#создание папок для датасета
def create_folders():
    """creates folders for datasets"""
    path_bad = os.path.join("dataset", "bad")
    if not os.path.isdir(path_bad):
        os.makedirs(path_bad)
    path_good = os.path.join("dataset", "good")
    if not os.path.isdir(path_good):
        os.makedirs(path_good)

#рандомная задержка
def slep():
    """makes a random or null delay"""
    global configs
    if configs['delay'] != 0:
        delay = random.uniform(10, 60)
        print(f'delay is: {delay}')
        time.sleep(delay)
    else: 
        print('delay is null')

def sync_configs():
    """saves current configs to the config file"""
    global configs
    with open("config.yaml", "w") as f:
        yaml.safe_dump(configs, f)
        
    


good_reviews = Template("https://www.kinopoisk.ru/film/${film_id}/reviews/ord/date/status/good/perpage/200/page/${page_num}/")
bad_reviews = Template("https://www.kinopoisk.ru/film/${film_id}/reviews/ord/date/status/bad/perpage/200/page/${page_num}/")
url = "https://www.kinopoisk.ru/top/navigator/m_act[rating]/1%3A/order/num_vote/perpage/200/#results"
chrome = UserAgent().chrome

def get_page(link: str) -> BeautifulSoup:
    """tries to get soup-page without captcha"""
    global chrome
    while True:
        html = requests.get(link, headers={'User-Agent': chrome}).text
        slep()
        page = BeautifulSoup(html, 'lxml')
        captcha = page.find_all('div', class_ = "CheckboxCaptcha")
        if (captcha is None) or len(captcha)==0:
            print("page is gotten")
            return page
        print("fail, is catpcha")

def save_rewievs_from_page(page: BeautifulSoup, film_name: str, good: bool):
    """Save rewievs for film from on of his page"""
    global configs
    rewievs = page.find_all('div', class_ = 'brand_words')
    count_key="count_of_good_rewievs"
    file_way = Template('dataset\\good\\${num}.txt')
    if not good:
        count_key = "count_of_bad_rewievs"
        file_way = Template('dataset\\bad\\${num}.txt')

    for i, rewiev in enumerate(rewievs):
        if configs[count_key]>=1000:
            break
        configs[count_key]+=1
        sync_configs()
        num = format(configs[count_key], '04d')
        with open(file_way.substitute(num = num), 'w+', encoding='utf8') as file:
            file.write(film_name+'\n'+rewiev.text)


def save_rewievs(film_id: str, film_name: str, good: bool):
    """saves good rewievs from one film"""
    global configs
    page_key = "page_num_good"
    if good:
        link = good_reviews.substitute(film_id = film_id, page_num=configs[page_key])
    else:
        page_key = "page_num_bad"
        link = bad_reviews.substitute(film_id = film_id, page_num=configs[page_key])
    page = get_page(link)
    
    #парсим количество хороших отзывывов
    count_of_rewievs = page.find('div', class_ = 'pagesFromTo')
    if count_of_rewievs is None:
        return 0
    count_of_rewievs = count_of_rewievs.text
    count_of_rewievs = int(re.sub('\d+.\d+ из ', '', count_of_rewievs, count=0))
    print(f"In film {film_name} {count_of_rewievs} {good} rewievs")

    #подсчет количества страниц с хорошими отзывами одного фильма ------#
    count_of_pages = 0
    if count_of_rewievs>=200:
        count_of_pages = count_of_rewievs//200
        if count_of_rewievs > count_of_pages*200:
            count_of_pages+=1
    else:
        count_of_pages = 1
    print(f'Count of pages with {good} rewievs for film "{film_name}" is {count_of_pages}')
    #------------------------------------------------------------------#

    save_rewievs_from_page(page, film_name, good)
    configs[page_key]+=1
    sync_configs()
    page_num = configs[page_key]
    for i in range(page_num, count_of_pages+1, 1):
        print(f"saving a {i} page")
        link = good_reviews.substitute(film_id = film_id, page_num=i)
        page = get_page(link)
        save_rewievs_from_page(page, film_name, good)
        configs[page_key]+=1
        sync_configs()
    configs[page_key]=1
    sync_configs()

        
if __name__=="__main__":
    get_configs()
    create_folders()
    films = {}
with open('films.json', 'r') as file:
    films = json.load(file)

#сохраняем хорошие рецензии
for key in films.keys():
    if configs["count_of_good_rewievs"] >=1000:
        break
    if configs["film_id"] == 0:
        configs["film_id"] = key
        sync_configs()
    elif configs["film_id"] != key:
        continue
    save_rewievs(key, films[key]["name"], True)
    configs["film_id"] = 0
    sync_configs()
    
#сохраняем плохие рецензии
for key in films.keys():
    if configs["count_of_bad_rewievs"] >=1000:
        break
    if configs["film_id"] == 0:
        configs["film_id"] = key
        sync_configs()
    elif configs["film_id"] != key:
        continue
    save_rewievs(key, films[key]["name"], False)
    configs["film_id"] = 0
    sync_configs()
    



