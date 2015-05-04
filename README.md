```
GPLv3
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/
```

# tinyMBS

## 安装依赖

apt-get install redis-server

## 文件目录介绍

```
#源码目录
-----pymbs #源码
-----tests #测试代码
-doc #文档
```

## 接口

### 推送数据 pushmsg

```
api : /pushmsg
param :
c_code 接收客户端 recv code
c_msg 消息  msg
return msgid
```

### 获取消息 listmsg

```
api: /listmsgs
param : client_code 接收客户端 recv code
return msglist
```

### 查询消息 getmsg

```
api: /getmsg/([0-9]+)
param : msgid
return msginfo
```

