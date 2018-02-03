import os
import sys
import random
from lxml import html
 

GET_CNN_NEWS_XPATH = """//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 'zn-body__paragraph')]//text()"""

user_agents = []
user_agents_file = os.path.join(os.path.dirname(__file__), 'user-agents.txt')
with open(user_agents_file, 'rb') as f:
    for line in f.readlines():
        if line:
            user_agents.append(line)
random.shuffle(user_agents)
#header
#random.shuffle
#random.choice
def get_header():
    ua = random.choice(user_agents)
    headers = {
        "connection":"close",
        "User-Agent":ua
    }
    return headers

#session.get()
def extract_news(news_url):
    session_request = requests.session()
    res = session_request.get(news_url, headers=get_header())
    news = {}
    try:
        tree = html.fromstring(res.content)
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception:
        return {}
    return news
