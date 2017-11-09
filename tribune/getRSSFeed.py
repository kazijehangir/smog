import feedparser

d = feedparser.parse('https://tribune.com.pk/feed/')

print(d['feed'])