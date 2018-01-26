import mongdb_client as client

#db.collections.Method
def test():
    db = client.get_db('news')
    db['news'].drop()
    db['news'].insert({'test': 1})
    db['news'].insert({'testa': 2})
    assert db['news'].count() == 2

if __name__ == "__main__":
    test()
