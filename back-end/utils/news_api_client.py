import requests
import json
import datetime

NEWS_API_ENDPOINT = "https://newsapi.org/v1/"
NEWS_API_KEY = '188a054cc3204b0487b3be93cd0234ee'
NEWS_NAME = 'articles'
DEFAULT_SOURCES = ['cnn']
SORT_BY_TOP = 'top'

def _buildUrl(endPoint=NEWS_API_ENDPOINT, searchName=NEWS_NAME):
    return endPoint + searchName

def getNews(sources=DEFAULT_SOURCES, apiKey=NEWS_API_KEY, sortBy=SORT_BY_TOP):
    articles = []
    for source in sources:
        payload = {'apiKey':apiKey,
                    'source':source,
                    'sortBy':sortBy}
        response = requests.get(_buildUrl(), params=payload)
        result_json = json.loads(response.content.decode('utf-8'))
        #result_json = response.json()
        # json.loads(response.content.decode('utf-8'))
        if result_json is not None and result_json['status'] == 'ok' and result_json['source'] is not None:
            for article in result_json['articles']:
                article['source'] = result_json['source']
                if article['publishedAt'] is None:
                    article['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                articles.append(article)
    return articles
