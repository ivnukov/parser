# -*- coding: utf-8 -*- 
import urllib.request, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "http://new.vk.com/search?c[group]=39626380&c[section]=people"

def get_full_html(url):
    browser = webdriver.Firefox()
    browser.get(url)
    scrolling_times =(find_user_quantity(get_html(url)))//30
    print(scrolling_times)
    result_div = browser.find_element_by_id("results")
    while scrolling_times:
        result_div.send_keys(Keys.END)
        scrolling_times-=1
    full_page = browser.page_source
    browser.close()
    return BeautifulSoup(full_page, 'lxml')
	
def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf8')

def parse(soup):
    table = soup.find_all('div', class_ = 'labeled name')
    users = []
    for user in table:
        users.append({
            'Имя': user.a.text,
            'Профайл': ("http//vk.com" + user.a.get("href")),
#           'Город': user.find_all('div', class_ = 'labeled')[1].text
            })
    return users

def find_user_quantity(html):
    soup = BeautifulSoup(html,'lxml')
    users_amount = (soup.find_all('span'))[:1]#, class_ = 'summary'))
    quantity = ''
    for i in str(users_amount):
        if i.isnumeric():
            quantity+=i
    return int(quantity)

def save_html(soup):
    f = open("vkhtml.html", 'w')
    f.write(soup.prettify())
    f.close
    print("done!")

def save_to_csv(users, path):
    with open(path , 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Имя', 'Ссылка на Профайл'))

        for user in users:
            writer.writerow((
                user['Имя'], 
                user['Профайл'],
                ))

def main():
    save_to_csv(parse(get_full_html(url)), 'vkpars.csv')

if __name__ ==	'__main__':
    main()