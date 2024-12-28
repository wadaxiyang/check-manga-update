import base64
import requests

def login(username, password, salt='123456'):
    # 加密
    password = base64.b64encode((password+'-'+salt).encode()).decode()
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
    print(token)

# 参数为用户名和密码
login('C321654987','abc12345')