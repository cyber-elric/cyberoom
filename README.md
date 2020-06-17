# 部署过程

<h3>Django	uWSGI	Nginx	https	openssl	ubuntu</h2>

<br/>

1. **申请阿里云服务器，并做简单配置，重置实例密码，配置安全组**

2. **通过SSH连接云服务器**

	```ssh root@0.0.0.0```

3. **创建系统新用户**
```
	adduser username
	再输入密码
```
4. **下载python3，安装pip**
```
	apt-get install python3.x
	apt-get install python3-pip 
```
将python默认指向python3.7
```
	update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
	update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
	update-alternatives --install /usr/bin/python python /usr/bin/python3.7 3
	update-alternatives --config python
```
5. **下载git**

	apt-get install git

6. **git clone 项目**

	```git clone https://github.com/you/project.git```

7. **安装项目所需的包，安装uwsgi时可能会出错**
```
	apt-get install python3.7-dev
	pip install -r requirements
```
测试uwsgi，新建test.py，如下
```
	def application(env, start_response):
		start_response = ('200 OK', [('Content-Type', 'text/html')])
		return[b'hello the world']  # python3
		# return ['hello world']  # python2
```
测试运行，在浏览器打开127.0.0.1:8001，看到hello world， 成功

	```uwsgi   --http :8001  --plugin python  --wsgi-file test.py```
	
<br/>

8. **更改django的settings.py**

生成django项目秘钥
```
	from django.core.management import utils
	SECRET_KEY = utils.get_random_secret_key()
```
生产环境配置
```
	DEBUG = False
	ALLOWED_HOSTS = ['*']
```
MySQL连接，不明文保存密码
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
my.cnf如下
```
	# my.cnf
	
	[client]
	database = databaseName
	user = userName
	password = userPassword
	host = hostName  # 默认localhost可不填
	port = 3306  # 默认3306可不填
	default-character-set = utf8
	
	!include ... # 文件原来的内容
	!include ... # 文件原来的内容
```
静态文件
```
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")
    
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```
<br/>

9. **安装MySQL**

	```apt-get install mysql-server```

首次登录MySQL，如果安装时没有设置密码，查看 /etc/mysql/debian.cnf，获取password

	```mysql -u debian-sys-maint -p password```

修改root用户的密码

	```update mysql.user set password=password('yourPassword')  where user='root' and host='localhost';```

10. **创建用户，授权；创建数据库要设置字符集为utf8**
```
	CREATE USER 'username'@'host' IDENTIFIED BY 'password';
	GRANT ALL ON *.* to 'username'@'host';
	
	CREATE DATABASE databaseName character set utf8;
```

mysql字符集命令
```
    show variables like 'char%';  # 当前MYSQL服务器字符集设置
    ALTER DATABASE databaseName DEFAULT CHARACTER SET 'utf8';  #更改
```

配置文件
```
	[client]
	default-character-set=utf8
	
	[mysql]
	default-character-set=utf8
	
	[mysqld]
	character-set-server=utf8
```
11. **将django项目中的数据库设计导入MySQL** 
```
	python mange.py makemigrations
	python manage.py migrate
```
测试运行项目，浏览器打开127.0.0.1:8000

	```python manage.py runserver```

通过uWSGI运行项目

	```uwsgi --http :8001 --module yourSite.wsgi:application```

12. **配置uWSGI，创建uwsgi.ini** 
```
	# cyberoom_uwsgi.ini file
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
	# harakiri = 20 
	
	# limit the project to 128 MB
	# limit-as = 128 
	
	# respawn processes after serving 5000 requests
	# max-requests = 5000 
	
	# background the process & log
	daemonize = /path/to/your/uwsgi.log
```
 通过uWSGI运行项目 
 
 	```
	uwsgi --ini uwsgi.ini
	```
控制uwsgi
	```
	uwsgi --reload uwsgi.pid
	uwsgi --stop uwsgi.pid
	```
13. **下载Nginx** 

	```apt-get install nginx```

14. **配置Nginx，在项目路径下创建yoursite_nginx.conf，将/etc/nginx/uwsgi_params复制到项目路径** 

```
	# yoursite_nginx.conf
	
	# the upstream component nginx needs to connect to
	upstream django {
		server unix:///path/to/your/site/yoursite.sock; # for a file socket
		#server 127.0.0.1:8001; # for a web port socket (we'll use this first)
	}
	
	# configuration of the server
	server {
		# the port your site will be served on
		listen      443;
		# the domain name it will serve for
		#server_name .example.com; # substitute your machine's IP address or FQDN
		
		# ssl on;
	    ssl_certificate /path/to/your/project/server.crt;
	    ssl_certificate_key /path/to/your/project/server.key;
		
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
	
15. **将上面nginx配置文件创建一个链接到/etc/nginx/sites-enabled ，可能需要权限，写绝对路径**

	```ln -s /path/to/your/site/yoursite_nginx.conf /etc/nginx/sites-enabled/```

控制nginx
	```
	nginx -t
	nginx -t -c test.conf
	systemctl start nginx
	nginx -s reload
	```
16. **使用openssl生成https证书**

    - 安装openssl

      ```
      apt-get install openssl
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

**未解决**

用pyperclip和clipboard将内容复制到粘贴板，未成功。

apt install了xsel和xclip，pip install了PyQt5都没用。
