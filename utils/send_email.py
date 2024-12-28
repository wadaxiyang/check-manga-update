from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# 定义一个服务对象,有地址、端口、授权码等属性
class EmailServer:
    def __init__(self, server_addr, server_port, email_token):
        self.addr = server_addr
        self.port = server_port
        self.token = email_token


def send_email(from_email, to_email, server:EmailServer, subject,content):
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
        smtp_server = smtplib.SMTP_SSL(server.addr, server.port)
        # smtp_server.set_debuglevel(1)  # 增加调试输出
        smtp_server.login(from_email, server.token)
        smtp_server.sendmail(from_email, to_email, msg.as_string())
        smtp_server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")


