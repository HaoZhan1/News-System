import pyjsonrpc

URL = "http://localhost:5050"

client = pyjsonrpc.HttpClient(
    url=URL
)

def getPreferenceForUser(userId):
    prefrence = client.call('getPreferenceForUser', userId)
    print("Preference List %s" % str(prefrence))
    return prefrence
