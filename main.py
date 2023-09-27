from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from string import Template
import time
import random
import os
import re

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
    


good_review_temp = Template("https://www.kinopoisk.ru/film/${film_id}/reviews/ord/date/status/good/perpage/10/page/${page_num}/")
bad_review_temp = Template("https://www.kinopoisk.ru/film/${film_id}/reviews/ord/date/status/bad/perpage/10/page/${page_num}/")
url = Template("https://www.kinopoisk.ru/top/navigator/m_act[rating]/1%3A/order/num_vote/page/${page}/#results") 



def get_divs(page_id: int) -> list:
    while True:
        slep()
        url_ = url.substitute(page = page_id)
        html_text = requests.get(url_, headers={'User-Agent': UserAgent().chrome}).text
        soup = BeautifulSoup(html_text, 'lxml')
        divs= soup.find_all('div', class_ = 'item _NO_HIGHLIGHT_')
        if len(divs)!=0:
            break
    return divs
    

films = {}
divs = get_divs(1)
for div in divs:
    film_id = div.get('id')
    film_id = re.search("\d+", film_id).group(0)
    films[film_id] = {}
    film_name = div.find('div', class_ = 'name')
    films[film_id]['rus_name'] = film_name.find('a').text
    films[film_id]['eng_name'] = film_name.find('span').text
    print(films[film_id])

