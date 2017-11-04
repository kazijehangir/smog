import urllib2
from bs4 import BeautifulSoup
import json
import time
import random
import threading

base_url = 'https://www.dawn.com/news/'
printLock = threading.Lock()


def scrapeArticles(thread_num):
    with printLock:
        print('Starting thread', thread_num)
    try:
        start = int(open('done_pc_' + str(thread_num) + '.txt', 'r')
                        .read().split()[-1].strip())
    except Exception as e:
        print('Exception', e)
        start = 128113
    done = open('done_pc_' + str(thread_num) + '.txt', 'a')

    outfile = open('dawn_articles_pc_' + str(thread_num) +
                   '.json', 'a')
    with printLock:
        print(thread_num, 'Starting with', start)

    while start < 136400:
        try:
            id = start * 10 + thread_num
            page = urllib2.urlopen(base_url + str(id))
            soup = BeautifulSoup(page, 'html.parser')

            article = soup.find('div', attrs={'class': 'story__content'}).text
            title = soup.find('h2', attrs={'class': 'story__title'}).text
            author = soup.find('span', attrs={'class': 'story__byline'}).text
            date = soup.find('span', attrs={'class': 'story__time'}).text
        except Exception as e:
            with printLock:
                print(id, 'Exception', e)
            continue

        json.dump(
            {id: {'article': article, 'title': title, 'author': author,
                'date': date}},
            outfile)
        outfile.write('\n')
        done.write(str(start))
        done.write('\n')
        with printLock:
            print(thread_num, 'got', id)
        time.sleep(random.uniform(1, 5))
        start += 1


for i in range(10):
    t = threading.Thread(target=scrapeArticles, args=(i,))
    t.start()
