import urllib2
from bs4 import BeautifulSoup
import json
import time
import random
import threading

base_url = 'https://www.dawn.com/news/'
printLock = threading.Lock()


def scrapeArticles(start, done, outfile):
    thread_num = 0
    with printLock:
        print('Starting thread', thread_num, "with", start)
    delay = 1
    while start < 1364000:
        try:
            id = start
            request = urllib2.Request(base_url + str(id), headers={'User-Agent': 'Mozilla/5.0'})
            page = urllib2.urlopen(request)
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
            done.write('\n')
            done.write(str(start))
            with printLock:
                print(thread_num, 'got', id)
            delay = 1
        except Exception as e:
            with printLock:
                try:
                    if e.code == 403:
                        start -= 1
                        delay += 1
                        print(id, thread_num, 'Exception', e, e.code, e.reason)
                except Exception as e2:
                    print (id, 'Exception', e)
        sleep = random.uniform(0, 3 * delay)
        with printLock:
            print(thread_num, 'sleeping with delay', delay, sleep)
        time.sleep(sleep)
        start += 1


start = int(open('done.txt', 'r')
                .read().split('\n')[-1].strip())

done = open('done.txt', 'a', 0)

outfile = open('dawn_articles_single.json', 'a')

scrapeArticles(start, done, outfile)
