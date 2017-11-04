import json
import re

def validDate(date):
    # return Bool
    # date: String
    # Valid dates: 
    # July 16 at 11:42am
    # 13 mins
    # 4 hrs
    # July 16, 2016 at 11:42am 
    pattern1 = r'\w+ [0-9]+ at [0-9]+:[0-9]+[am|pm].*'
    pattern2 = r'[0-9]+ mins.*'
    pattern3 = r'[0-9]+ hrs.*'
    pattern4 = r'\w+ [0-9]+, [0-9]+ at [0-9]+:[0-9]+[am|pm].*'
    if re.match(pattern1, date) or re.match(pattern2, date) or re.match(pattern3, date) or re.match(pattern4, date):
        # print('Accepted date:', date)
        return True
    # print('Rejecting date: ', date)
    return False

all_articles = {}
articles = open('dawn_articles.json', 'r').read().strip().split('\n')
for article in articles:
    try:
        # print('JSON loading: ', prof.strip())
        article = json.loads(article.strip())
        # print('JSON: ', prof)
        for k in article.keys():
            all_articles[k] = article[k]
    except Exception as e:
        print('Excpetion:', e)
        continue

allPostsOutput = open('allArticles.json', 'w')
json.dump(all_articles, allPostsOutput)
print('Got ', len(all_articles.keys()), ' articles.')

keywords = ['smog', 'polution', 'air', 'breathing']
filtered = {}
for id in all_articles.keys():
    found = False
    article = all_articles[id]
    for keyword in keywords:
        if (keyword in article['article'].split(' ') or
            keyword in article['title'].split(' ')):
                found = True
    if found:
        filtered[id] = all_articles[id]

print('Filtered articles: ', len(filtered.keys()))

outputFiltered = open('filteredArticles.json', 'w')
json.dump(filtered, outputFiltered)
