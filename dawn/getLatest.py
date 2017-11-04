import urllib2
from bs4 import BeautifulSoup
import json
import time
import random

base_url = 'https://www.dawn.com/news/'

id = int(open('done.txt', 'r').read().split()[-1].strip())
done = open('done.txt', 'w')
outfile = open('dawn_articles.json', 'a')

while id > 0:
    try:
        page = urllib2.urlopen(base_url + str(id))
        soup = BeautifulSoup(page, 'html.parser')

        article = soup.find('div', attrs={'class': 'story__content'}).text
        title = soup.find('h2', attrs={'class': 'story__title'}).text
        author = soup.find('span', attrs={'class': 'story__byline'}).text
        date = soup.find('span', attrs={'class': 'story__time'}).text
        json.dump(
            {id: {'article': article, 'title': title, 'author': author,
                  'date': date}},
            outfile)
        outfile.write('\n')
    except Exception as e:
        print('Exception', e)

    if id % 10 == 0:
        done.write(str(id))
        done.write('\n')
    time.sleep(random.uniform(1, 5))
    id -= 1

