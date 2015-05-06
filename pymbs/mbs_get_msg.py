import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import redis

class GetMsgHandler(tornado.web.RequestHandler):
    def init_db_redis(func):
        def fn(self,input):
            self.db = redis.Redis(connection_pool=self.application.pool)
            func(self,input)
        return fn

    @init_db_redis
    def get(self,msgid):
        if not msgid > 0 :
            data = {'retcode':404,'retmsg':'not found'}
            data_json = json.dumps(data)
            print data_json
            self.write(data_json)
            return
        else:
            ret = self.db.exists('tinymbs:msgbox:%s'%(msgid))
            if ret:
                ret_list = self.db.get('tinymbs:msgbox:%s'%(msgid))
                ret_data = json.dumps(ret_list)
                self.write(ret_data)
            else:
                data = {'retcode':404,'retmsg':'not found'}
                data_json = json.dumps(data)
                print data_json
                self.write(data_json)

    def on_finish(self):
        del self.db
