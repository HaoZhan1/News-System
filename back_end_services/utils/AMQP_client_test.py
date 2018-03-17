from AMQP_client import CloudAMQPClient

URL = "amqp://svowqrcq:HFkG2SlMhRFeIuGKUjJTo7nGYkcnhzOj@termite.rmq.cloudamqp.com/svowqrcq"
QUEUE_NAME = "test"

def test():
    client = CloudAMQPClient(URL, QUEUE_NAME)
    message = {"hhh" : "hhh"}
    client.sendMessage(message)
    receiveMessage = client.receiveMessage()
    assert message == receiveMessage
    print ("passed!")

if __name__ == "__main__":
    test()
