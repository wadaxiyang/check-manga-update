import requests
import json

def login(username, password, salt, vars):
    url = "https://www.mangacopy.com/api/kb/web/login"
    # 请求体
    data = {
        "username": username, # 用户名
        "password": password, # 密码
        "salt": salt # 盐
    }
    # 请求头
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", url, headers=headers, data=data)
    # 解析响应的 JSON 数据
    response_data = response.json()
    # 提取 token
    token = response_data['results']['token']
    with open(vars, 'r') as file:
        var_data = json.load(file)
    var_data['token'] = token
    # 保存 token 到 var.json
    with open(vars, 'w') as file:
        json.dump(var_data, file, indent=4)
    print('登录成功!')
    return token  