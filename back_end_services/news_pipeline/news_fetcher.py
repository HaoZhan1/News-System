import os
import sys
import news_scraper
from newspaper import Article


SLEEP_TIME_IN_SECOND = 10
RECEIVE_QUEUE_URL = 'amqp://svowqrcq:HFkG2SlMhRFeIuGKUjJTo7nGYkcnhzOj@termite.rmq.cloudamqp.com/svowqrcq'
RECEIVE_QUEUE_NAME = 'news-test'
FETCH_QUEUE_URL = 'amqp://txggakbg:Ds_nOkznHFtnSnCGX3xwb9VlYkD-LDZY@llama.rmq.cloudamqp.com/txggakbg'
FETCH_QUEUE_NAME = 'fect_news'

sys.path.append(os.path.join(os.path.dirname('__file__'),'..','utils'))
from AMQP_client import CloudAMQPClient

scraper_news_queue_client = CloudAMQPClient(RECEIVE_QUEUE_URL, RECEIVE_QUEUE_NAME)
fecth_news_queue_client = CloudAMQPClient(FETCH_QUEUE_URL, FETCH_QUEUE_NAME)

def handle_message(msg):
    if not msg or not isinstance(msg, dict):
        print('msg in broken')
        return
    text = None
    #if msg['source'] == 'cnn':
        #text = news_scrapter.extract_news(msg['url'])
    #else:
        #print('News source [%s] is not supported.' % msg['source'])
    #Download article according the url
    article = Article(msg['url'])
    article.download()
    article.parse()
    msg['text'] = article.text
    #sendMessage
    fecth_news_queue_client.sendMessage(msg)


while True:
    #receive message
    if scraper_news_queue_client:
        msg = scraper_news_queue_client.receiveMessage()
        if msg:
            try:
                #handle message
                handle_message(msg)
            except Exception as e:
                print(e)
        fecth_news_queue_client.sleep(SLEEP_TIME_IN_SECOND)
