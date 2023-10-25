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

def get_page(link: str) -> str:
    """return a html of page with rewievs"""
    global chrome
    slep()
    html_text = requests.get(link, headers={'User-Agent': chrome}).text
    return html_text

def save_rewievs_from_page(page: BeautifulSoup, film_name: str):
    """Save rewievs for film from on of his page"""
    global configs
    rewievs = page.find_all('div', class_ = 'brand_words')
    for i, rewiev in enumerate(rewievs):
        if configs["count_of_good_rewievs"]>=1000:
            break
        configs["count_of_good_rewievs"]+=1
        sync_configs()
        num = format(i+configs["count_of_good_rewievs"], '04d')
        with open(f'dataset\\good\\{num}.txt', 'w+', encoding='utf8') as file:
            file.write(film_name+'\n'+rewiev.text)

def save_good_rewievs(film_id: str, film_name: str, stop_page: int = 0):
    html = ''
    page = None
    count_of_rewievs = 0
    while True:
        link = good_reviews.substitute(film_id = film_id, page_num =1)
        html = get_page(link)
        print(f"try to get page of {film_name}")
        page = BeautifulSoup(html, 'lxml')
        count_of_rewievs = page.find('div', class_ = 'pagesFromTo')
        if count_of_rewievs is not None:
            sync_configs()
            break
    count_of_rewievs = count_of_rewievs.text
    count_of_rewievs = int(re.sub('\d+.\d+ из ', '', count_of_rewievs, count=0))
    print(f"In film {film_name} {count_of_rewievs} good rewievs")

    #подсчет количества страниц одного фильма
    count_of_pages = 0
    if count_of_rewievs>=200:
        count_of_pages = count_of_rewievs//200 #получаем количетсво страниц с отзывами
        if count_of_pages > count_of_rewievs*200:
            count_of_pages+=1
    else:
        count_of_pages = 1
    ####

    print(f"Count of pages with good rewievs for film {film_name} is {count_of_pages}")
    rewievs = page.find_all('div', class_ = 'brand_words')
    for i, rewiev in enumerate(rewievs):

        




if __name__=="__main__":
    get_configs()
    create_folders()
    films = {}
with open('films.json', 'r') as file:
    films = json.load(file)
    save_good_rews("1143242", films["1143242"]['name'])
