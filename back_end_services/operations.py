import json
import os
import sys
import pickle
import redis
from datetime import datetime
from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname('__file__'),'utils'))
from AMQP_client import CloudAMQPClient
import mongodb_client
import news_recommandation_client

NEWS_TABLE_NAME = "newstest"
NEWS_LIST_BATCH_SIZE = 20
NEWS_LIMIT = 200
USER_NEWS_TIME_OUT_IN_SECONDES = 60

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

LOG_CLICKS_TASK_QUEUE_URL = 'amqp://cvarabcw:vVIPYEFWkVLhAv3t6osMtdwOMhnKAnu6@llama.rmq.cloudamqp.com/cvarabcw'
LOG_CLICKS_TASK_QUEUE_NAME = 'tap-news-log-clicks-task-queue'
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def getOneNews():
    db = mongodb_client.get_db()
    news = db[NEWS_TABLE_NAME].find_one()
    #news is bson
    return json.loads(dumps(news))


def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE
    slice_news = []
    #redis to store user_id : digestList
    #for bson bson.dumps()
    if redis_client.get(user_id):
        #pickle.loads() from string to python object
        total_news_digest = pickle.loads(redis_client.get(user_id))
        slice_news_digest = total_news_digest[begin_index:end_index]
        db = mongodb_client.get_db()
        slice_news = db[NEWS_TABLE_NAME].find({'digest':{'$in': slice_news_digest}})
    else:
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt',-1)]).limit(NEWS_LIMIT))
        total_news_digest = [news['digest'] for news in total_news]
        redis_client.set(user_id, pickle.dumps(total_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDES)
        slice_news = total_news[begin_index:end_index]
        #bson.dumps change from bson to json
    preferences = news_recommandation_client.getPreferenceForUser(user_id)
    #add the topPreference & today news
    topPreference = None
    if preferences and len(preferences) > 0:
        topPreference = preferences[0]
    today_date = str(datetime.now().date())
    for news in slice_news:
        if 'class' in news and news['class'] == topPreference:
            news['reason'] = 'Recommand'
        if today_date in str(news['publishedAt']):
            news['time'] = 'today'
    return json.loads(dumps(slice_news))

def logNewsClickForUser(user_id, news_id):
    message = {'userId': user_id,'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    print(message)
    cloudAMQP_client.sendMessage(message)
