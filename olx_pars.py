# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup as bs
import csv
import datetime

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.170"
}

base_url = "https://www.olx.ua/nedvizhimost/kvartiry-komnaty/arenda-kvartir-komnat/kharkov/?search%5Bdistrict_id%5D=69"


def olx_parse(base_url, headers):
    global start
    start = datetime.datetime.now()
    urls = []
    urls.append(base_url)
    ads = []
    #использую сессию
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    #проверка ответа от сервера
    if request.status_code == 200:
        soup = bs(request.content, "lxml")
        try:
            #определение последней страницы
            last_page = soup.find('a', attrs={'data-cy': 'page-link-last'})['href']
            num = list(last_page)
            number_of_last_page = str(num[-2])+str(num[-1])
            #итерация по всем страницам
            for i in range(int(number_of_last_page)-1):
                url = f'{base_url}&page={i+2}' #первая страница соответствует базовому "base_url",а страницы с "page=0" не существует, поэтому отсчет начинается с "page=2"
                #добавление URL всех страниц в список
                if url not in urls:
                    urls.append(url)
        except:
            pass

        #итерация по всем страницам
        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            trs = soup.find_all('tr', attrs={'class': 'wrap'}) #поиск всех классов с объявлениями
            #итерация по каждому объявлению
            for tr in trs:
                try:
                    #сбор информации
                    title = tr.find('a', attrs={'class': 'marginright5 link linkWithHash detailsLink'}).text
                    href = tr.find('a', attrs={'class': 'marginright5 link linkWithHash detailsLink'})['href']
                    price = tr.find('p', attrs={'class': 'price'}).text
                    ads.append({
                        'title': title,
                        'url': href,
                        'price': price,
                    })


                except:
                    pass

    else:
        print('Error')
    end = datetime.datetime.now()
    print(f"Время выполнения парсинга: {end-start}")
    return ads


def files_writer(ads):
    with open('parsed_advertisement.csv', 'w+') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Заголовок', 'Ссылка на объявление', 'Цена'))
        for ad in ads:
            a_pen.writerow((ad['title'], ad['url'], ad['price']))
    endwrite = datetime.datetime.now()
    print(f"Время выполнения всей программы: {endwrite - start}")


ads = olx_parse(base_url, headers)
files_writer(ads)
