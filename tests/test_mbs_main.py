import urllib2
import json
import pdb
import redis

def test_redis_get_msgid():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    db = redis.Redis(connection_pool=pool)
    myid = db.incr('tinymbs:msgid')
    print myid
    print type(myid)

def test_mbs_main_post():
    http_url = "http://127.0.0.1:8000/pushmsg"
    data = {'c_code' : 'applist','c_msg':'abc','c_id':0}
    jdata = json.dumps(data)
    print jdata
    http_request = urllib2.Request(http_url,jdata)
    http_response = urllib2.urlopen(http_request)
    print http_response.read()
    http_response.close()

def test_mbs_main_list():
    http_url = "http://127.0.0.1:8000/listmsgs?client_code=applist"
    http_response = urllib2.urlopen(http_url)
    print http_response.read()
    http_response.close()

def test_mbs_main_get():
    http_url = "http://127.0.0.1:8000/listmsgs?client_code=applist"
    http_response = urllib2.urlopen(http_url)
    print http_response.read()
    http_response.close()

if __name__ == "__main__":
    test_mbs_main_post()

# req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
# f = urllib2.urlopen(req)
# response = f.read()
#f.close()
