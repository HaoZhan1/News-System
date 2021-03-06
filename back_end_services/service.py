""" service backend"""
import os
import sys
import json
from bson.json_util import dumps
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import operations

sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
import mongodb_client

#crate rpcServer and register Method
SERVER_HOST = 'localhost'
SERVER_POST = 4041

def add(num1, num2):
    return num1 + num2

def get_one_new():
    print("you are getting one news")
    news = mongodb_client.get_db()['news'].find_one()
    return json.loads(dumps(news))

def getNewsSummariesForUser(user_id, page_num):
    print('ddddd')
    return operations.getNewsSummariesForUser(user_id, page_num)

def logNewsClickForUser(user_id, news_id):
    return operations.logNewsClickForUser(user_id, news_id)

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_POST))
#registerMethod
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(get_one_new, 'get_one_new')
RPC_SERVER.register_function(getNewsSummariesForUser, 'getNewsSummariesForUser')
RPC_SERVER.register_function(logNewsClickForUser, 'logNewsClickForUser')
RPC_SERVER.serve_forever()
