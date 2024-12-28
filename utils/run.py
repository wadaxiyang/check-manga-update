import json
import os
from utils.send_email import send_email
from utils.api_request import fetch_comics

def run(username, password, salt, vars,from_email, to_email, server,token):
    try:
        os.chdir('data')
    except FileNotFoundError:
        pass
    comics ='comics.json'
    flag,response = fetch_comics(username, password, salt,token, vars)
    # print(response)
    try:
        with open(comics, 'r', encoding='utf-8') as file:
            comics_data = json.load(file)
            # 比较response内容与comics.json内容
            if response == comics_data:
                print("无更新😢")
                return
    except (FileNotFoundError, json.JSONDecodeError):
        # 更新comics.json文件内容
        print("文件不存在，创建comics.json文件")
        with open(comics, 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=4)

    # 更新comics.json文件内容
    print("有更新！😋")
    with open(comics, 'w', encoding='utf-8') as file:
        json.dump(response, file, ensure_ascii=False, indent=4)

    # 生成邮件内容
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
    message += "</table>"
    # token失效
    if flag:
        message += "<h2>token失效，请更新</h2>"
    message+="</body></html>"
    subject = '有漫画更新了🥰'
    # 发送邮件
    send_email(from_email, to_email, server, subject,message)