import ConfigParser

def load_config_setting(cfg = None):
    config = {}
    config['setting'] = {}
    config['mode'] = {}
    config['logging'] = {}
    if cfg is None:
        cfg = r"/etc/mbs/config/default.conf"
        cfg = r'/home/ndk/myhome/github/tinyMBS/config/ex.conf'
    cfg_parser = ConfigParser.ConfigParser()
    cfg_parser.readfp(open(cfg))
    config['setting']['timeout'] = cfg_parser.get('setting','timeout',0)
    config['setting']['db_ip'] = cfg_parser.get('setting','db_ip',"10.3.3.19")
    config['setting']['db_port'] = cfg_parser.get('setting','db_port',6379)
    config['setting']['db_name'] = cfg_parser.get('setting','db_name',0)
    config['setting']['server_port'] = cfg_parser.get('setting','server_port',0)
    config['setting']['server_ip'] = cfg_parser.get('setting','server_ip',"0.0.0.0")
    config['mode']['debug'] = cfg_parser.get('mode','debug',False)
    config['logging']['log_file'] = cfg_parser.get('logging','log_file')
    return config

if __name__ == "__main__":
    print load_config_setting()
