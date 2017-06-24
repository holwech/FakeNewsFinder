
# coding: utf-8

# In[ ]:


import feedparser as fp
import json
import newspaper
from newspaper import Article
from collections import namedtuple
from time import mktime
from datetime import datetime

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")
data = {}
data['newspapers'] = {}

with open('NewsPapersRSS.json') as data_file:
    RSS = json.load(data_file)

count = 1
for company, value in RSS.items():
    if 'rss' in value:
        d = fp.parse(value['rss'])
        print("Downloading articles from ", company)
        newsPaper = {
            "rss": value['rss'],
            "link": value['link'],
            "articles": []
        }
        for entry in d.entries:
            if hasattr(entry, 'published'):
                if count > 400:
                    break
                article = {}
                article['link'] = entry.link
                date = entry.published_parsed
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    print(e)
                    print("continuing...")
                    continue
                article['title'] = content.title
                article['text'] = content.text
                newsPaper['articles'].append(article)
                print(count, "articles downloaded from", company, ", url: ", entry.link)
                count = count + 1
    else:
        print("Building site for ", company)
        paper = newspaper.build(value['link'], memoize_articles=False)
        newsPaper = {
            "link": value['link'],
            "articles": []
        }
        noneTypeCount = 0
        for content in paper.articles:
            if count > 400:
                break
            try:
                content.download()
                content.parse()
            except Exception as e:
                print(e)
                print("continuing...")
                continue
            if content.publish_date is None:
                print(count, " Article has date of type None...")
                noneTypeCount = noneTypeCount + 1
                if noneTypeCount > 10:
                    print("Too many noneType dates, aborting...")
                    noneTypeCount = 0
                    break
                count = count + 1
                continue
            article = {}
            article['title'] = content.title
            article['text'] = content.text
            article['link'] = content.url
            article['published'] = content.publish_date.isoformat()
            newsPaper['articles'].append(article)
            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
            count = count + 1
            noneTypeCount = 0
    count = 1
    data['newspapers'][company] = newsPaper


# In[ ]:


try:
    with open('scraped_articles_rss.json', 'w') as outfile:
        json.dump(data, outfile)
except Exception as e: print(e)





