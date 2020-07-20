# 部署过程

<h3>Django	uWSGI	Nginx	https	openssl	ubuntu</h2>
  

1. **创建系统新用户**

```
adduser username
再输密码
```

   

2. **apt换源**

```
sudo mv /etc/apt/sources.list /etc/sources.list.backup
sudo vim /etc/apt/sources.list
```

将对应版本的Ubuntu的国内源粘贴上去，例Ubuntu20.04，阿里云源

```
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
```



3. **python & pip**

```
sudo apt install python3.x
sudo apt install python3-pip 
```
- pip换源

Linux

```
mkdir ~/.pip
vim ~/.pip/pip.conf

# 文件内容
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
# 下面的不知有没有作用
# [install]
# trusted-host = mirrors.aliyun.com
```

Win10

```
md C:\Users\yourName\pip
notepad C:\Users\yourName\pip\pip.ini

# 文件内容
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
# 下面的不知有没有作用
# [install]
# trusted-host = mirrors.aliyun.com
```

- 设置python默认指向

```
# python
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2
sudo update-alternatives --config python

# pip
sudo update-alternatives -install /usr/bin/pip pip /usr/bin/pip3.7 1
sudo update-alternatives -install /usr/bin/pip pip /usr/bin/pip3.8 2
sudo update-alternatives --config pip
```



4. **git**

- 安装

```
sudo apt install git
```

- git clone 项目，安装需要的库

```
git clone https://github.com/you/project.git
pip install -r requirements.txt
```

*如果GitHub太慢了，可以将项目复制到码云，再clone

教程：[https://zhuanlan.zhihu.com/p/111697412](https://zhuanlan.zhihu.com/p/111697412)

```
git clone https://gitee.com/you/project.git
```



5. **Django**

- 更改django的settings.py

```
cp sample_settings.py settings.py
cp sample_urls.py urls.py
```

- 生成django项目密钥

```
# 运行python
from django.core.management import utils
SECRET_KEY = utils.get_random_secret_key()

# 通过此函数得到密钥后，将密钥复制到settings.py中的
SECRET_KEY = ''
```
- 生产环境配置

```
DEBUG = False
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['EXAMPLE.COM']  # ???
```
- MySQL连接，不明文保存密码

```
import pymysql

pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS':{
            'read_default_file': '/etc/mysql/my.cnf'
        },
    }
}
```
*my.cnf在下一步

- 静态文件

```
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
    
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# urls.py

from django.conf.urls.static import static
from django.conf import settings
# from django.conf.urls import url
# from django.views import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^static/(?P<path>.*)$', static.serve,
    #     {'document_root': settings.STATIC_ROOT}, name='static')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- 404 & 500

```
# urls.py

handler404 = 'gate.views.page_not_found'
handler500 = 'gate.views.page_error'
```



6. **MySQL**

- 安装

```
sudo apt install mysql-server
```

- 首次登录MySQL，如果安装时没有设置密码，查看 /etc/mysql/debian.cnf，获取password

```
sudo cat /etc/mysql/debian.cnf
mysql -u debian-sys-maint -p
```

- 修改root用户的密码

```
# 新版
update mysql.user set authentication_string = 'yourPassword' where user = 'root';  
# 旧版
update mysql.user set password=password('yourPassword')  where user='root';
```

- 创建用户，授权；创建数据库要设置字符集为utf8

```
CREATE USER 'username'@'host' IDENTIFIED BY 'yourPassword';
GRANT ALL ON *.* to 'username'@'host';
CREATE DATABASE databaseName default character set = 'utf8';
```

- my.cnf

```
# ...文件原内容

# my.cnf

[client]
database = databaseName
user = userName
password = userPassword
host = hostName  # 默认localhost可不填
port = 3306  # 默认3306可不填
default-character-set = utf8

!include ... # 文件原内容
!include ... # 文件原内容
```

```
# 3个MySQL配置文件
[client]
default-character-set=utf8

[mysql]
default-character-set=utf8

[mysqld]
character-set-server=utf8
```
*mysql字符集命令

```
show variables like 'char%';  # 当前MYSQL服务器字符集设置
ALTER DATABASE databaseName DEFAULT CHARACTER SET 'utf8';  #更改
```



7. **migrate**

- 将django项目中的数据库设计导入MySQL

```
python manage.py makemigrations
python manage.py migrate
```
*此时可以测试运行项目，浏览器打开127.0.0.1:8000

```
python manage.py runserver
```

*可能会出现MySQL错误

```
vim /home/userName/.local/lib/python3.x/sites-packages/django/db/backends/mysql/base.py

# 将这两行注释掉

if version < (1, 3, 13):
    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
```



8. **uwsgi**

- 安装

```
sudo apt install uwsgi
```

*安装uwsgi时可能会出错

```
sudo apt install python3.x-dev
```



测试uwsgi，新建test.py，如下

```
def application(env, start_response):
	start_response = ('200 OK', [('Content-Type', 'text/html')])
	return[b'hello the world']  # python3
	# return ['hello world']  # python2
```

测试运行，在浏览器打开127.0.0.1:8001，看到hello world， 成功

```
uwsgi   --http :8001  --plugin python  --wsgi-file test.py
```

通过uwsgi运行django项目

```
uwsgi --http-socket 0.0.0.0:8000 --plugin python3 --module yourSite.wsgi:application
```



- 配置uwsgi，创建uwsgi.ini

```
# uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir =  /your/project/path 

# Django's wsgi file
module = yourSite.wsgi:application 

# the socket (use the full path to be safe
socket = /path/to/your/site.sock
# socket = 127.0.0.1:8001

# ... with appropriate permissions - may be needed
chmod-socket = 664

# be the same as nginx's
# uid = www-data
# gid = www-data

# the virtualenv (full path)
# home = /path/to/virtualenv

# master
master = true         

# maximum number of worker processes
processes = 4

buffer-size = 30000

# clear environment on exit
vacuum = true

# set an environment variable
# env = DJANGO_SETTINGS_MODULE=mysite.settings 

# create a pidfile
pidfile =  /path/to/your/uwsgi.pid  

# respawn processes taking more than 20 seconds
harakiri = 66

# limit the project to 128 MB
# limit-as = 128 

# respawn processes after serving 5000 requests
max-requests = 666 

# background the process & log
# disable-logging = true
daemonize = /path/to/your/uwsgi.log

# plugin = python38
```
 通过uwsgi运行项目 

```
uwsgi uwsgi.ini  # 启动
uwsgi --ini uwsgi.ini  #启动
uwsgi --reload uwsgi.pid  #重加载
uwsgi --stop uwsgi.pid  #停止
```



9. **Nginx**

- 安装

```
sudo apt install nginx
```

- 配置Nginx，在项目路径下创建yoursite_nginx.conf，将/etc/nginx/uwsgi_params复制到项目路径

```
# nginx.conf

# the upstream component nginx needs to connect to
upstream django {
	server unix:///path/to/your/site/yoursite.sock; # for a file socket
	#server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

# configuration of the server
server {
	# the port your site will be served on
	listen		443 ssl;
	# listen      443;
		
	# ssl on;
	ssl_certificate /path/to/your/project/server.crt;
	ssl_certificate_key /path/to/your/project/server.key;
	
	# the domain name it will serve for
	#server_name .example.com; # substitute your machine's IP address or FQDN
	
	charset     utf-8;

	# max upload size
	client_max_body_size 75M;   # adjust to taste

	# Django media
	location /media  {
		alias /path/to/your/site/media;  # your Django project's media files - amend as required
	}

	location /static {
		alias /path/to/your/site/static; # your Django project's static files - amend as required
	}
	
	# Finally, send all non-media requests to the Django server.
	location / {
		uwsgi_pass  django;
		include     /path/to/your/site/uwsgi_params; # the uwsgi_params file you installed
	}
}
```

- 将上面nginx配置文件创建一个链接到/etc/nginx/sites-enabled ，写绝对路径

```
sudo ln -s /path/to/your/site/yoursite_nginx.conf /etc/nginx/sites-enabled/
```

*如果没有启用uwsgi.ini中的uid和gid，就要修改nginx的配置

```
sudo vim /etc/nginx/nginx.conf

user yourUserName;
# user www-data;
```

*控制nginx

```
nginx -t
nginx -t -c test.conf
nginx -s reload
nginx -s stop

sudo /etc/init.d/nginx start | stop | restart
sudo service nginx start | stop | restart
sudo systemctl start | stop | restart nginx
```



10. **使用openssl生成https证书**

- 安装openssl

  ```
  sudo apt install openssl
  ```

- 创建私钥

  ```
  openssl genrsa -des3 -out server.key 2048
  ```

- 创建签名请求证书CSR

  ```
  openssl req -new -key server.key -out server.csr
  ```

- 在加载SSL支持的Nginx并使用上述私钥时除去必须的口令

  ```
  cp server.key server.key.org
  openssl rsa -in server.key.org -out server.key
  ```

- 标记证书使用上述私钥和CSR

  ```
  openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
  ```







# Error

1. uwsgi命令行启动项目时，识别不出‘--module'选项

解决方法：

安装uwsgi-plugin-python3,根据python版本选择版本

然后启动时在’--module'选项前加上'--plugin python3'




