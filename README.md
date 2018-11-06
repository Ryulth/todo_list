# TODO LIST
사용자의 할일 목록을 보여주고 작성 및 수정 가능하게 한다.
## DEMO
* [유튜브](https://youtu.be/q8WqLHNbvHw)
* [TODO 사이트](http://todo.ryulth.com)
* DEMO ID : DEMO
* DEMO PW : DEMO
## Architecture
![todo_ar](https://user-images.githubusercontent.com/32893340/47960711-86460800-e042-11e8-991d-dc38fee04b45.png)
## 개발환경

* python3
* mysql5.x

## 배포환경

* nginx
* docker
* docker-compose
* Ubuntu 16.04.5 LTS (Xenial Xerus)

## 공통 설정
```bash
git clone https://github.com/Ryulth/todo_list.git
cd todo_list
vim mysql.cnf
```

* mysql.cnf 파일 작성

```bash
#mysql.cnf

[client]

DATABASE:'db_name'
USER:'user_name'
PASSWORD:'user_pw'
HOST: 'host_name'
PORT:'3306 or other port'
default-character-set=utf8

```
```bash
pip3 install -r requirements.txt
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
```

## 1)Python 자체 구동
* sudo python3 manage.py runserver 
localhost:8000 or servername:8000 확인
## 2)NGINX + django 연동 구동

### NGINX 설정

* Nginx 설치 [nginx install](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)

* sudo vim /etc/nginx/site-available/todo 

```bash
upstream todo{
    server unix:/path/to/project/todo_list/todo.sock; 
}

server {
    listen 80;
    listen [::]:80;
    server_name server_name or localhost;
    charset utf-8;
    location /static {
             alias /path/to/project/todo_list/todo/static;
    }

    location / {
    include        /etc/nginx/uwsgi_params;
    uwsgi_pass      todo;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/todo /etc/nginx/sites-enabled/
sudo /etc/init.d/nginx restart
```
### Docker 구동
```bash
docker-compose -f docker-compose-todo.yml up -d
```
localhost:80 or servername:80 확인

