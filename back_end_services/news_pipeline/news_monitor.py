import sys
import os
import redis
import hashlib

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'utils'))
#method
import news_api_client
#class
from AMQP_client import CloudAMQPClient

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3
SLEEP_TIME_TASK_SECONDS = 10

NEWS_SOURCES = [
    'bbc-newson',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]
#redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

#AMQP_client
QUEUE_URL = "amqp://svowqrcq:HFkG2SlMhRFeIuGKUjJTo7nGYkcnhzOj@termite.rmq.cloudamqp.com/svowqrcq"
QUEUE_NAME = "news-test"
cloudAMQP_client = CloudAMQPClient(QUEUE_URL, QUEUE_NAME)

#while
while True:
    news_list = news_api_client.getNews(NEWS_SOURCES)
    number_of_news = 0
    for news in news_list:
        #redis to prevent duplicate
        #use md5 for title
        news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()
        if not redis_client.get(news_digest):
            number_of_news = number_of_news + 1
            news['digest'] =  news_digest
            redis_client.set(news_digest, 'hh')
            #set expire time
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)
            #send message to queue
            cloudAMQP_client.sendMessage(news)
    print('%s number of news' % number_of_news)
    #sleep
    cloudAMQP_client.sleep(SLEEP_TIME_TASK_SECONDS)
