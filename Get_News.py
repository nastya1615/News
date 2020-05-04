import json

import requests
from bs4 import BeautifulSoup

URL = 'https://xn--80aesfpebagmfblc0a.xn--p1ai/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    link = []
    time = []
    text = []

    name_of_news = {}
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('section', {'class': 'cv-section', 'id': 'news'})  # достали часть кода про новости

    for item in items:
        new_items = item.find_all('li', {'class': "cv-news-list__item"})
        for new_item in new_items:
            lin = new_item.find('a').get('href')
            if lin[0:5] == 'news/':
                lin = URL + lin
                link.append(lin)
            else:
                link.append(lin)
            tim = new_item.find('div').get_text()
            time.append(tim)
            name_of_news = new_item.find('h4').get_text()
            text.append(name_of_news)
    get_json_from_link(text, content_from_news(link), link, time)


def content_from_news(link):
    text_massive = []
    for content in range(len(link)):
        try:
            html = get_html(link[content])
            soup = BeautifulSoup(html.text, "html.parser")
            items = soup.find('div', {'class': "cv-full-news__text"})
            item = items.find_all("p")
            text = ''
            for item_str in item:
                text += '\n' + item_str.get_text()
                text_massive.append(text)
        except:
            text = "Читайте информацию по ссылке\n" + link[content]
            text_massive.append(text)
    return text_massive


def get_json_from_link(name_of_news, text, link, time, ):
    news = {}
    for i in range(len(link)):
        news[name_of_news[i]] = {
            'text': text[i],
            'link': link[i],
            'time': time[i],

        }
    with open('news.json', 'w') as f:
        json.dump(news, f, indent=2)


def pars():
    html = get_html(URL)
    # try:
    if html.status_code == 200:
        get_content(html.text)

    # except:
    #   print("Error")


if __name__ == '__main__':
    pars()
