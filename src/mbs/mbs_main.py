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
        pass

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

    def __request2json(func):
        def fn(self):
            if len(self.request.body):
                try:
                    self.no_error = True
                    self.req_json_packet = json.loads(self.request.body)
                    if not self.req_json_packet['c_code']:
                        self.no_error = False
                    elif not self.req_josn_packet['c_msg']:
                        self.no_error = False
                except ValueError, e:
                    self.no_error = False
                    print e
                except KeyError, e:
                    self.no_error = False
                    print e
                except AttributeError , e:
                    self.no_error = False
                    print e
                finally:
                    func(self)
                    print "ending"
        return fn

    @__request2json
    @init_db_redis
    def post(self):
        if not self.no_error :
            data = {'retcode':404,'retmsg':'not found'}
            data_json = json.dumps(data)
            print data_json
            self.write(data_json)
        else:
            self.db.set('remote_ip:%s'%(self.request.remote_ip),"%s"%(self.request.body))
            self.write(self.request.body)

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

    def __request2json(func):
        def fn(self):
            if len(self.request.body):
                try:
                    self.req_json_packet = json.loads(self.request.body)
                except ValueError, e:
                    print e
                else:
                    print self.req_json_packet
                    print "ending"
                    func(self)
        return fn

    # @init_db_redis
    # def post(self):
    #     self.__request2json()
    #     self.db.set('remote_ip:%s'%(self.request.remote_ip),"%s"%(self.request.body))
    #     self.write(self.request.body)

    @init_db_redis
    def get(self):
        data = {'retcode':000,'msg':self.db.get('remote_ip:%s' %(self.request.remote_ip))}
        data_json = json.dumps(data)
        self.write(data_json)


if __name__ == "__main__":
    tornado.options.parse_command_line()
#    app = tornado.web.Application(handlers=[(r"/", IndexHandler),(r"/pushmsg",PushMsgHandler)])
    app = RunMain()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
