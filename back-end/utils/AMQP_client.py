import pika
import json

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        #connection
        self.connectionParams = pika.URLParameters(self.cloud_amqp_url)
        self.connection = pika.BlockingConnection(self.connectionParams)
        #channel & queue
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = queue_name)
    #basic_publish
    def sendMessage(self, message):
        self.channel.basic_publish(exchange = '',
                                   routing_key = self.queue_name,
                                   body = json.dumps(message))
        print("Send message to %s : %s" % (self.queue_name, message))

    #basic_get & basic_ack
    def receiveMessage(self):
        #callback
        method, params, body = self.channel.basic_get(self.queue_name)
        if method:
            print("Receive message from %s : %s" % (self.queue_name, body.decode('utf-8')))
            self.channel.basic_ack(method.delivery_tag)
            #convert B yte to String
            return json.loads(body.decode('utf-8'))
        else:
            print("No message get")
            return None

    def sleep(self, seconds):
        self.connection.sleep(seconds)
