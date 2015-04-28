import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import redis
import pdb

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class RunMain(tornado.web.Application):
    def __init__(self):
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        handlers = [(r"/pushmsg", PushMsgHandler),(r"/listmsgs", GetMsgHandler)]
        tornado.web.Application.__init__(self, handlers, debug=True)

class IndexHandler(tornado.web.RequestHandler):
    def post(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

class PushMsgHandler(tornado.web.RequestHandler):
    def init_db_redis(func):
        def fn(self):
            self.db = redis.Redis(connection_pool=self.application.pool)
            func(self)
        return fn

    def http_buffer_to_json(func):
        def fn(self):
            if len(self.request.body):
                try:
                    self.no_error = True
                    self.req_json_packet = json.loads(self.request.body)
                    if not self.req_json_packet['c_code']:
                        self.no_error = False
                    elif not self.req_json_packet['c_msg']:
                        self.no_error = False
                except ValueError, e:
                    self.no_error = False
                    print e
                except KeyError, e:
                    self.no_error = False
                except AttributeError , e:
                    self.no_error = False
                finally:
                    func(self)
                    print self.req_json_packet
        return fn

    @http_buffer_to_json
    @init_db_redis
    def post(self):
        print self.req_json_packet
        if not self.no_error :
            data = {'retcode':404,'retmsg':'not found'}
            data_json = json.dumps(data)
            self.write(data_json)
        else:
            self.req_json_packet['c_id'] = self.db.incr('tinymbs:msgid')
            self.db.lpush('tinymbs:channel:%s'%(self.req_json_packet['c_code']),"%s"%(self.req_json_packet))
            self.db.set('tinymbs:msgbox:%s'%(self.req_json_packet['c_id']),"%s"%(self.req_json_packet))
            self.write(self.req_json_packet)

    def get(self):
        data = {'retcode':404,'retmsg':'not found'}
        data_json = json.dumps(data)
        self.write(data_json)

class GetMsgHandler(tornado.web.RequestHandler):
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
            print data_json
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
                print data_json
                self.write(data_json)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = RunMain()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
