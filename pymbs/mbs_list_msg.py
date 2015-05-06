import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import redis
import pdb

class ListMsgHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.no_error = False

    def init_db_redis(func):
        def fn(self):
            self.db = redis.Redis(connection_pool=self.application.pool)
            func(self)
        return fn

    @init_db_redis
    def get(self):
        client_code = self.get_argument('client_code', None)
        if not client_code :
            data = {'retcode':404,'retmsg':'not found'}
            data_json = json.dumps(data)
            self.write(data_json)
            return
        else:
            ret = self.db.exists('tinymbs:channel:%s'%(client_code))
            if ret:
                ret_list = self.db.lrange('tinymbs:channel:%s'%(client_code),0,10)
                ret_data = json.dumps(ret_list)
                self.write(ret_data)
            else:
                data = {'retcode':404,'retmsg':'not found'}
                data_json = json.dumps(data)
                self.write(data_json)

    def on_finish(self):
        del self.db
