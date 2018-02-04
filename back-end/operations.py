import json
import os
import sys
import pickle
import redis
import datetime
from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname('__file__'),'utils'))
from AMQP_client import CloudAMQPClient
import mongodb_client

NEWS_TABLE_NAME = "newstest"
NEWS_LIST_BATCH_SIZE = 10
NEWS_LIMIT = 200
USER_NEWS_TIME_OUT_IN_SECONDES = 60

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

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
    #for bson pickle.loads() bson.dumps()
    if redis_client.get(user_id):
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
    return json.loads(dumps(slice_news))
