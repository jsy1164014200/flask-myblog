# flask my blog 

## jwt认证

这里的演示是 `Flask-JWT` 的 Quickstart内容。

安装必要的软件包：

```
pip install flask
pip install Flask-JWT
```

一个简单的 DEMO：

```python
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id="%s")" % self.id

users = [
    User(1, "user1", "abcxyz"),
    User(2, "user2", "abcxyz"),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode("utf-8"), password.encode("utf-8")):
        return user

def identity(payload):
    user_id = payload["identity"]
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "super-secret"

jwt = JWT(app, authenticate, identity)



def protected():
    return "%s" % current_identity

if __name__ == "__main__":
    app.run()
```

首先需要获取用户的 JWT：

```
% http POST http://127.0.0.1:5000/auth username="user1" password="abcxyz"             ~
HTTP/1.0 200 OK
Content-Length: 193
Content-Type: application/json
Date: Sun, 21 Aug 2016 03:48:41 GMT
Server: Werkzeug/0.11.10 Python/2.7.10

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDcxNzUxMzIxLCJuYmYiOjE0NzE3NTEzMjEsImV4cCI6MTQ3MTc1MTYyMX0.S0825N6IliQb65QoJfUXb3IGq-j9OVJpHBh-bcUz_gc"
}
```

使用 `@jwt_required()` 装饰器来保护你的 API

```
def protected():
    return "%s" % current_identity
```

这时候你需要在 HTTP 的 header 中使用 `Authorization: JWT `才能获取数据

```
% http http://127.0.0.1:5000/protected Authorization:"JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDcxNzUxMzIxLCJuYmYiOjE0NzE3NTEzMjEsImV4cCI6MTQ3MTc1MTYyMX0.S0825N6IliQb65QoJfUXb3IGq-j9OVJpHBh-bcUz_gc"
HTTP/1.0 200 OK
Content-Length: 12
Content-Type: text/html; charset=utf-8
Date: Sun, 21 Aug 2016 03:51:20 GMT
Server: Werkzeug/0.11.10 Python/2.7.10

User(id="1")
```

不带 JWT 的时候会返回如下信息：

```python
% http http://127.0.0.1:5000/protected                                                ~
HTTP/1.0 401 UNAUTHORIZED
Content-Length: 125
Content-Type: application/json
Date: Sun, 21 Aug 2016 03:49:51 GMT
Server: Werkzeug/0.11.10 Python/2.7.10
WWW-Authenticate: JWT realm="Login Required"

{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```

## 数据库设计

### 评论

| 字段名    | 类型     | 说明    |
| --------- | -------- | ------- |
| _id       | ObjectId | 代替id  |
| username  | string   |         |
| content   | string   |         |
| create_at | data     |         |
| blog_id   | string   | blog_id |

博客

| 字段名       | 类型     | 说明                   |
| ------------ | -------- | ---------------------- |
| _id          | ObjectId | 自带id                 |
| blog_id      | string   |                        |
| title        | string   |                        |
| summary      | string   |                        |
| content      | string   |                        |
| read_size    | int      |                        |
| comment_size | int      |                        |
| tags         | string   | 以逗号分开             |
| create_at    | date     |                        |
| update_at    | date     |                        |
| catalogs     | [list]   | 分类                   |
| username     | String   | 表示用户的（未来加入） |

