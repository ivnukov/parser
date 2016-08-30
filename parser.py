import csv
import urllib.request
from bs4 import BeautifulSoup

URL = 'https://www.weblancer.net/jobs/'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def get_page_count(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('ul', class_ = 'pagination')
    last_page = (str(pages.find_all('a')[-1]))
    counter = ''
    for i in last_page:
        if i.isnumeric():
            counter+=i
    return (int(counter))

def parse(html):
    soup = BeautifulSoup(html,'lxml')
    table = soup.find('div', class_ = 'cols_table')
    rows = table.find_all('div', class_ = 'row')
    projects = []
    for row in rows:
        projects.append({
            "title": row.a.text,
            "category": [category.text for category in row.div.find_all('a', class_ = 'text-muted')],
            "price": row.find('div', class_ = 'amount').text.strip(),
            "call": row.find('div', class_ = 'text-nowrap').text.strip(),
            "link": ('https://www.weblancer.net' + row.a.get("href"))
            })
        return projects 

def save_to_csv(projects, path):
    with open(path , 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Project', 'Category', 'Price', 'Calls', 'link'))

        for project in projects:
            writer.writerow((
                project['title'], 
                ', '.join(project['category']),
                project['price'], 
                project['call'],
                project['link']
                ))

def save_html(soup):
    f = open("parnik.html", 'w')
    f.write(soup.prettify())
    f.close
    print("done!")

def main():
    page_count = get_page_count(get_html(URL))
    print('Pages found: %d' % page_count)

    projects = []
	
    for page in range(page_count):
        print('Complete %d%%'  %(page/page_count*100))
        projects.extend(parse(get_html(URL+"?page=%d" % page)))

    save_to_csv(projects, 'projects.csv')

if __name__  == '__main__':
    main()

