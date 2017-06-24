
# coding: utf-8

# In[ ]:


import feedparser as fp
import json
import newspaper
from newspaper import Article
from collections import namedtuple

data = {}
data['newspapers'] = {}


# In[ ]:


with open('NewsPapersRSS.json') as data_file:
    RSS = json.load(data_file)


# In[ ]:


count = 1
for company, value in RSS.items():
    print("Downloading articles from ", company)
    d = fp.parse(value['rss'])
    newsPaper = {
        "rss": value['rss'],
        "articles": []
    }
    for entry in d.entries:
        if hasattr(entry, 'published'):
            article = {}
            article['link'] = entry.link
            article['published'] = entry.published
            content = Article(entry.link)
            content.download()
            content.parse()
            article['title'] = content.title
            article['text'] = content.text
            newsPaper['articles'].append(article)
            print(count, "articles downloaded from", company, ", url: ", entry.link)
            count = count + 1
    count = 1
    data['newspapers'][company] = newsPaper


# In[ ]:


try:
    with open('scraped_articles_rss.json', 'w') as outfile:
        json.dump(data, outfile)
except:
    print('Sad :(')


# In[ ]:



# In[ ]:





# In[ ]:





# In[ ]:




