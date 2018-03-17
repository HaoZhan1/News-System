import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
import mongodb_client
from AMQP_client import CloudAMQPClient

SLEEP_TIME_IN_SECOND = 10
FETCH_QUEUE_URL = 'amqp://txggakbg:Ds_nOkznHFtnSnCGX3xwb9VlYkD-LDZY@llama.rmq.cloudamqp.com/txggakbg'
FETCH_QUEUE_NAME = 'fect_news'
NEWS_TABLE_NAME = "newstest"

cloudAMQP_client = CloudAMQPClient(FETCH_QUEUE_URL, FETCH_QUEUE_NAME)
SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

def handle_mesage(msg):
    if not msg or not isinstance(msg, dict):
        return
    text = msg['text']
    if not text:
        return
    print(msg)
    #get the start and end time of this day and find list in db
    published_at = parser.parse(msg['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days = 1)
    db = mongodb_client.get_db()
    same_day_news_list = list(db[NEWS_TABLE_NAME].find({
        'publishedAt':{'$gte':published_at_day_begin, '$lt':published_at_day_end}
    }))
    #if there is news in the same date, validate the duplicate
    if same_day_news_list and len(same_day_news_list) > 0:
        documents = [news['text'] for news in same_day_news_list]
        documents.insert(0, text)

        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        rows, cols = pairwise_sim.shape
        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print('duplicate news.Ignore')
                return

        msg['publishedAt'] = published_at
        db[NEWS_TABLE_NAME].replace_one({'digest' : msg['digest']}, msg, upsert=True)
    else:
        msg['publishedAt'] = published_at
        db[NEWS_TABLE_NAME].replace_one({'digest' : msg['digest']}, msg, upsert=True)


while True:
    if cloudAMQP_client:
        msg = cloudAMQP_client.receiveMessage()
        if msg:
            try:
                handle_mesage(msg)
            except Exception as e:
                print(e)
        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECOND)
