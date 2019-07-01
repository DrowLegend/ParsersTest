import requests
from bs4 import BeautifulSoup as bs
import csv

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.170"
}

base_url = "https://kharkov.hh.ua/search/vacancy?clusters=true&currency_code=UAH&enable_snippets=true&text=Python&area=2206&from=cluster_area"


def hh_parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, "lxml")
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://kharkov.hh.ua/search/vacancy?L_is_autosearch=false&area=5&clusters=true&currency_code=UAH&enable_snippets=true&text=Frontend&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
            for div in divs:
                try:
                    title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                    href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                    company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                    jobs.append({
                        'title': title,
                        'href': href,
                        'company': company
                    })
                except:
                    pass

        print(jobs)
    else:
        print("Error")
    return jobs




def files_writer(jobs):
    with open('parsed_jobs.csv', 'w+') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название вакансии', 'Ссылка на вакансию', 'Название компании'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company']))


jobs = hh_parse(base_url, headers)
files_writer(jobs)



