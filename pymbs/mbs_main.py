from pymbs.utils.config import load_config_setting
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import redis
import pdb

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

from mbs_push_msg import PushMsgHandler
from mbs_list_msg import ListMsgHandler
from mbs_get_msg import GetMsgHandler

class RunMain(tornado.web.Application):
    def __init__(self,db_port=6379,db_ip="localhost",db_name=0,debug_mode=False):
        self.pool = redis.ConnectionPool(host=db_ip, port=db_port, db=db_name)
        handlers = [(r"/pushmsg", PushMsgHandler),(r"/listmsgs", ListMsgHandler),(r'/getmsg/([0-9]+)',GetMsgHandler)]
        tornado.web.Application.__init__(self, handlers, debug=debug_mode)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    config = load_config_setting()
    app = RunMain(db_port=config['setting']['db_port'],db_ip=config['setting']['db_ip'],db_name=config['setting']['db_name'],debug_mode=config['mode']['debug'])
    http_server = tornado.httpserver.HTTPServer(app)
    if config['setting']['db_port'] == options.port :
        http_server.listen(options.port)
    elif config['setting']['db_port'] is not None:
        http_server.listen(config['setting']['server_port'],config['setting']['server_ip'])
    else:
        http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
