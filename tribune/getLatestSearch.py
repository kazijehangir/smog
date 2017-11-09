import urllib
import urllib2
from bs4 import BeautifulSoup
import json
import time
import random
import threading
from duckduckgo import search

def getCompleteUrl(query):
    time.sleep(1)
    try:
        print('Searching for:', query)
        for j in search(query, max_results=10):
            if j.startswith(query):
                return j
            else:
                print('result:', j)      
    except Exception as e:
        print('Exception in search:', e)

base_url = 'https://tribune.com.pk/story/'
printLock = threading.Lock()


def scrapeArticles(start, done, outfile):
    thread_num = 0
    with printLock:
        print('Starting thread', thread_num, "with", start)
    delay = 1
    while start > 0:
        try:
            url = getCompleteUrl(base_url + str(start))
            print('Got url:', url, 'for', start)
            if url:
                request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                page = urllib2.urlopen(request)
                soup = BeautifulSoup(page, 'html.parser')

                article = soup.find('div', attrs={'class': 'clearfix story-content read-full'}).text
                title = soup.find('h1', attrs={'class': 'title'}).text
                author = soup.find('div', attrs={'class': 'author'}).text
                date = soup.find('div', attrs={'class': 'timestamp'}).text
                json.dump(
                    {start: {'article': article, 'title': title, 'author': author,
                        'date': date}},
                    outfile)
                outfile.write('\n')
                delay = 1
                with printLock:
                    print(thread_num, 'got', start)
            else:
                delay = 0

            done.write('\n')
            done.write(str(start))

        except Exception as e:
            with printLock:
                try:
                    if e.code == 403:
                        start -= 1
                        delay += 1
                        print(start, thread_num, 'Exception', e, e.code, e.reason)
                    elif e.code == 404:
                        delay = 0
                    print(start, 'Exception', e, e.code, e.reason)
                except Exception as e2:
                    print (start, 'Exception', e)
        sleep = random.uniform(0, 3 * delay)
        with printLock:
            print(thread_num, 'sleeping with delay', delay, sleep)
        time.sleep(sleep)
        start -= 1


start = int(open('done.txt', 'r')
                .read().split('\n')[-1].strip())

done = open('done.txt', 'a', 0)

outfile = open('tribune_articles_single.json', 'a')

scrapeArticles(start, done, outfile)
