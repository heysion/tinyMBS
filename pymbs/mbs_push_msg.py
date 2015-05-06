import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import redis
import pdb

class PushMsgHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.no_error = False
        self.req_json = {}
        self.init_db_redis()
        self.http_buffer_to_json()
        if not self.no_error :
            del self.db

    def init_db_redis(self):
        self.db = redis.Redis(connection_pool=self.application.pool)

    def http_buffer_to_json(self):
        print self.request.body
        if len(self.request.body):
            try:
                self.no_error = True
                self.req_json = json.loads(self.request.body)
                if not self.req_json['c_code']:
                    self.no_error = False
                elif not self.req_json['c_msg']:
                    self.no_error = False
            except ValueError, e:
                self.no_error = False
                print e
            except KeyError, e:
                self.no_error = False
            except AttributeError , e:
                self.no_error = False
            finally:
                pass

    def post(self):
        if not self.no_error :
            data = {'retcode':404,'retmsg':'not found'}
            data_json = json.dumps(data)
            self.write(data_json)
        else:
            self.req_json['c_id'] = self.db.incr('tinymbs:msgid')
            self.db.lpush('tinymbs:channel:%s'%(self.req_json['c_code']),"%s"%(self.req_json))
            self.db.set('tinymbs:msgbox:%s'%(self.req_json['c_id']),"%s"%(self.req_json))
            self.write(self.req_json)

    def get(self):
        data = {'retcode':404,'retmsg':'not found'}
        data_json = json.dumps(data)
        self.write(data_json)

    def on_finish(self):
        if self.no_error:
            del self.db
