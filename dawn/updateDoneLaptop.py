for i in range(10):
    articles = open('dawn_articles_laptop_' + str(i) + '.json', 'r')
    article = articles.read().split('\n')[-1]
    id = article[2:8]
    done = open('done_laptop_' + str(i) + '.txt', 'a')
    print(i, 'adding', id)
    done.write('\n' + id)
