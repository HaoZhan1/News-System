import news_classes
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
import mongodb_client
from AMQP_client import CloudAMQPClient

LOG_CLICKS_TASK_QUEUE_URL = 'amqp://cvarabcw:vVIPYEFWkVLhAv3t6osMtdwOMhnKAnu6@llama.rmq.cloudamqp.com/cvarabcw'
LOG_CLICKS_TASK_QUEUE_NAME = 'tap-news-log-clicks-task-queue'
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)
db = mongodb_client.get_db()
NEWS_TABLE_NAME = "newstest"
PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
SLEEP_TIME_IN_SECONDS = 10
NUM_OF_CLASSES = 17
INITIAL_P = 1.0 / NUM_OF_CLASSES
ALPHA = 0.1

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return
    if 'userId' not in msg or 'newsId' not in msg or 'timestamp' not in msg:
        return
    userId = msg['userId']
    newsId = msg['newsId']
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({"userId": userId})
    #if user is not in the database
    if not model:
        print('create preference model for new user: %s' % userId)
        new_model = {'userId': userId}
        preferences = {}
        for item in news_classes.classes:
            preferences[item] = float(INITIAL_P)
        new_model['preference'] = preferences
        model = new_model
    print("Updating preference model for new user: %s" % userId)
    #if news don't have class
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if not news or 'class' not in news or not news['class']:
        print('skipping....')
        return
    click_class = news['class']
    #change the value of preference
    model['preference'][click_class] = float((1 - ALPHA) * model['preference'][click_class] + ALPHA)
    for item in model['preference']:
        if item != click_class:
            model['preference'][item] = float((1 - ALPHA) * model['preference'][item])
    #update
    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)

#consume message
def run():
    while True:
        if cloudAMQP_client:
            msg = cloudAMQP_client.receiveMessage()
            if msg:
                try:
                    handle_message(msg)
                except Exception as e:
                    raise
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
if __name__ == "__main__":
    run()
