from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from string import Template
import time
import random
import os
import re
import json

def create_folders():
    path_bad = os.path.join("dataset", "bad")
    if not os.path.isdir(path_bad):
        os.makedirs(path_bad)
    path_good = os.path.join("dataset", "good")
    if not os.path.isdir(path_good):
        os.makedirs(path_good)

def slep():
    delay = random.uniform(10, 60)
    print(f'delay is: {delay}')
    time.sleep(delay)
    


good_reviews = Template("https://www.kinopoisk.ru/film/${film_id}/reviews/ord/date/status/good/perpage/200/page/${page_num}/")
bad_reviews = Template("https://www.kinopoisk.ru/film/${film_id}/reviews/ord/date/status/bad/perpage/200/page/${page_num}/")
url = "https://www.kinopoisk.ru/top/navigator/m_act[rating]/1%3A/order/num_vote/perpage/200/#results"
chrome = UserAgent().chrome

def get_page(link: str) -> str:
    global chrome
    slep()
    html_text = requests.get(link, headers={'User-Agent': chrome}).text
    return html_text


    
create_folders()
films = {}
with open('films.json', 'r') as file:
    films = json.load(file)

count_of_good_revs = 0
for film_id in films.keys():
    html = ''
    soup = None
    rev_count = 0
    while True:
        link = good_reviews.substitute(film_id = film_id, page_num=1)
        html = get_page(link)
        print(f'film_id: {film_id}')
        soup = BeautifulSoup(html,'lxml')
        rev_count = soup.find('div', class_ = 'pagesFromTo')
        print(rev_count)
        if rev_count is not None:
            rev_count = rev_count.text
            count_of_good_revs+=50
            break
    rev_count = int(re.sub('\d+.\d+ из ', '', rev_count, count=0))
    print(rev_count)
    pages_count = rev_count//200
    if rev_count>pages_count*200:
        pages_count+=1
    print(f"pages_count: {pages_count}")

    good_revs = soup.find_all('div', class_ = 'brand_words')
    print(f"good_revs: {good_revs[0]}")
    for i, rev in enumerate(good_revs):
        num = format(i, '04d')
        with open(f'dataset\\good\\{num}.txt', 'w+', encoding='utf8') as file:
            file.write(films[film_id]['name']+'\n'+rev.text)

    for i in range(2, pages_count+1):
        while True:
            link = good_reviews.substitute(film_id = film_id, page_num=i)
            html = get_page(link)
            soup = BeautifulSoup(html,'lxml')
            test = soup.find('div', class_ ='pagesFromTo')
            print(test)
            if test is not None:
                count_of_good_revs+=50
                break
        good_revs = soup.find_all('div', class_ = 'brand_words')
        for j, rev in enumerate(good_revs):
            num = format((i-1)*200+j, '04d')
            with open(f'dataset\\good\\{num}.txt', 'w+', encoding='utf8') as file:
                file.write(films[film_id]['name']+'\n'+rev.text)
            
