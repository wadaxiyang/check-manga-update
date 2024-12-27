import base64

password = "abc12345"
salt = "123456"
password = base64.b64encode((password+'-'+salt).encode()).decode()

print(password)
