import http.client
import json
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from datetime import datetime

username, password, from_email, to_email, token = "", "", "", "", ""
salt = "123456" # 盐

# vars = 'test.json'
vars = 'var.json'

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


def login():
    global username, password, salt, vars
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
    with open(vars, 'w') as file:
        json.dump(var_data, file, indent=4)
    print('登录成功!')
    return token  

def send_email(content):
    global from_email, to_email, email_token
    subject = '今日漫画更新'
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # 将HTML内容添加到邮件
    msg.attach(MIMEText(content, 'html'))

    # 发送邮件
    try:
        # 设置SMTP服务器并登录
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(from_email, email_token)  # 这里的密码是QQ邮箱的授权码
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")

def api_request(token):
    conn = http.client.HTTPSConnection("www.mangacopy.com")
    headers = {
        'Authorization': f'Token {token}'
    }
    # print(headers)
    conn.request("GET", "/api/v3/member/collect/comics?ordering=-datetime_updated", headers=headers)
    res = conn.getresponse()
    data = res.read()
    if res.status == 401:
        print("token无效，正在尝试重新登录！")
        return False
    else :
        return json.loads(data.decode("utf-8"))

def fetch_comics():
    global token
    response = api_request(token)
    if response == False:
        token = login()
        response = api_request(token)
    return response

def run():
    response = fetch_comics()
    # print(response)

    try:
        with open('comics.json', 'r', encoding='utf-8') as file:
            comics_data = json.load(file)
            # 比较response内容与comics.json内容
            if response == comics_data:
                print("无更新（悲） :(")
                return
    except (FileNotFoundError, json.JSONDecodeError):
        # 更新comics.json文件内容
        print("文件不存在，创建comics.json文件")
        with open('comics.json', 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=4)

    print("有更新（乐） :)")
    with open('comics.json', 'w', encoding='utf-8') as file:
        json.dump(response, file, ensure_ascii=False, indent=4)
            
    message = """
    <html>
    <body>
    <h2>今日漫画更新</h2>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>漫画</th>
            <th>上次看到</th>
            <th>最新章节</th>
            <th>更新时间</th>
        </tr>
    """
    for comic in response['results']['list']:
        last_browse_name = ""
        name = comic['comic']['name'][:10]
        update_date = comic['comic']['datetime_updated']
        if comic['last_browse']:
            last_browse_name = comic['last_browse']['last_browse_name'][:10]
        last_chapter = comic['comic']['last_chapter_name'][:10]
        path_word = comic['comic']['path_word']
        message += f"""
                    <tr>
                        <td><a href='https://www.mangacopy.com/comic/{path_word}'>{name}</a></td>
                        <td>{last_browse_name}</td>
                        <td>{last_chapter}</td>
                        <td>{update_date}</td>
                    </tr>
                    """
    message += "</table></body></html>"
    send_email(message)

run()