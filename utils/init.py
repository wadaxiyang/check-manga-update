import json
import base64
import os

def init(vars,salt):
    os.chdir('data')
    with open(vars, 'r', encoding='utf-8') as file:
        data = json.load(file)
        username = data['username']
        password = data['password']
        from_email = data['from_email']
        to_email = data['to_email']
        token = data['token']
        email_token = data['email_token']
        # 对密码进行加密
        password = base64.b64encode((password+'-'+salt).encode()).decode()
    return username, password, from_email, to_email, token, email_token
