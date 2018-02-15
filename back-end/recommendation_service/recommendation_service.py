import os
import sys
import operator
import pyjsonrpc

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))
import mongodb_client
PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"

SERVER_HOST = 'localhost'
SERVER_PORT = 5050

def isclose(a, b, rel_tol = 1e-09):
    return abs(a - b) <= rel_tol * max(abs(a), abs(b))

class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def getPreferenceForUser(self, user_id):
        db = mongodb_client.get_db()
        model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'user_id': user_id})
        #no user in the database
        if not model:
            return []
        sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)
        sorted_list = [item[0] for item in sorted_tuples]
        sorted_value_list = [item[1] for item in sorted_tuples
        #make no sense
        if isclose(float(sorted_value_list[0]), float(sorted_value_list[0])):
            return []
        return sorted_list



server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print("Starting HTTP server ...")
server.serve_forever()
