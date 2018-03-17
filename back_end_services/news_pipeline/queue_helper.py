import os
import sys

#change the file path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from AMQP_client import CloudAMQPClient

QUEUE_URL = "amqp://svowqrcq:HFkG2SlMhRFeIuGKUjJTo7nGYkcnhzOj@termite.rmq.cloudamqp.com/svowqrcq"
QUEUE_NAME = "news-test"
FETCH_QUEUE_URL = 'amqp://txggakbg:Ds_nOkznHFtnSnCGX3xwb9VlYkD-LDZY@llama.rmq.cloudamqp.com/txggakbg'
FETCH_QUEUE_NAME = 'fect_news'
def clear_queue(queue_url, queue_name):
    queue_client = CloudAMQPClient(queue_url, queue_name)
    num_of_messages = 0
    while True:
        if queue_client:
            message = queue_client.receiveMessage()
            if message:
                num_of_messages = num_of_messages + 1
            else:
                print("%s num_of_messages" % num_of_messages)
                #return
                return

if __name__ == "__main__":
    clear_queue(FETCH_QUEUE_URL, FETCH_QUEUE_NAME)
