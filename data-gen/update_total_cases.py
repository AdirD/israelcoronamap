import random
from csv import writer

import lxml.html as lh
from datetime import date, timedelta

import requests
from requests.exceptions import ProxyError

URL_CASES_BY_COUNTRY = "https://www.worldometers.info/coronavirus/#countries"
PROXIES = [
    "198.199.119.119:3128",
    "3.14.250.195:80",
    "165.227.215.71:8080",
    "67.205.149.230:8080",
    "192.241.245.207:3128",
    "24.106.221.230:53281",
    "75.146.218.153:55768",
]


def update_total_cases_csv():
    response = proxy_get_request(URL_CASES_BY_COUNTRY)
    total_cases_israel = get_total_cases_by_country(response.text, 'israel')
    previous_day = date.today() - timedelta(days=1)
    new_row = [previous_day, total_cases_israel]
    with open('../public/data/total_cases_israel.csv', 'a+') as f:
        csv_writer = writer(f)
        csv_writer.writerow(new_row)


def proxy_get_request(url):
    while PROXIES:
        proxy_index = random.randint(0, len(PROXIES) - 1)
        try:
            response = requests.get(url, proxies={
                'http': PROXIES[proxy_index],
                'https': PROXIES[proxy_index]
            })
            return response
        except ProxyError:
            print('proxy %s failed' % PROXIES[proxy_index])
            PROXIES.pop(proxy_index)


def get_total_cases_by_country(page_html, country_name):
    table = lh.fromstring(page_html).xpath('//*[@id="main_table_countries"]')[0]
    countries_rows = table.xpath('tbody/tr')
    countries_rows.pop(0)
    for row in countries_rows:
        country_info = row[0]
        if hasattr(country_info, 'text') and country_name in country_info.text_content().lower():
            return int(row[1].text)
