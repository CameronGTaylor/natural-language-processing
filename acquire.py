import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import os
import re

def get_blog_articles(urls):
    def get_blog_article(url):
        headers = {'User-Agent': 'manual search'} 
        response = get(url, headers=headers)
        soup = BeautifulSoup(response.content)
        title = soup.select('title')[0].text
        selection = 'div > div.jupiterx-post-content.clearfix'
        article = soup.select(selection)
        article = article[0].text.replace('\xa0', ' ')
        return dict({'title': title, 'content': article})
    return [get_blog_article(url) for url in urls]

def get_inshorts_category_articles(url):
    lm = pd.DataFrame()
    headers = {'User-Agent': 'manual search'} 
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    for i in range(len(soup.select('span[itemprop=headline]'))):
        lm=lm.append({
            'title': soup.select('span[itemprop=headline]')[i].text, 
            'author': soup.select('span[class=author]')[i].text,
            'article': soup.select('div[itemprop=articleBody]')[i].text,
            'date': soup.select('span[clas=date]')[i].text, 
            'category': re.search(r'[a-z]+$', url)[0]},
            ignore_index=True)
    return lm

def get_news_articles(categories):
    df = pd.DataFrame()
    category_urls = [('https://inshorts.com/en/read/') + category \
                 for category in categories]
    for url in category_urls:
        df = df.append(get_inshorts_category_articles(url))
    return df