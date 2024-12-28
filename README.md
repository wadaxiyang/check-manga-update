# 定时获取拷贝漫画更新

## 简介

使用`Github Actions`定期执行python脚本检查个人书架的漫画是否更新，并使用邮件进行通知

## 怎么使用

- clone本仓库,**将仓库设为private**(因为仓库中会存放一些令牌和密码，不要fork，否则不能改成私有)

- 开启邮件SMTP服务，此处使用QQ邮箱，可以参阅[邮箱开启SMTP服务](https://clb.pages.dev/2024/12/27/开启SMTP服务/)获取邮箱授权码

- 修改仓库中的`copymanga/var.json`文件,将git绑定到你github的一个私有仓库并推送，大功告成

  > token	   拷贝漫画的token，**不必修改**，会自动生成
  > username	拷贝 用户名 	必须
  > password	拷贝 密码   	必须
  > from_email      发件人	      必须
  > to_email	收件人	      必须，可以发给自己
  > email_token     邮箱授权码	   必须
  
  ```json
  {
      "token": "lalala",
      "username": "98765432",
      "password": "123456",   			
      "from_email": "example@qq.com",		
      "to_email": "example@qq.com",		
      "email_token": "jlegvgancaltbijc"
  }
  ```
  
- 邮件提醒示例

  ![image-20241228101807069](https://s2.loli.net/2024/12/28/QAyn9otF82c3zfO.png)

## 修改其他配置

### 修改触发条件

> 触发条件默认是 7点-23点，每隔3小时触发一次，你可以调整触发频率或时间段，例如：
>
> `- cron: "0 7-23 * * *"` : 7-23 每小时触发一次

```yml
on:
  # 定时触发
  schedule:
    # 7点-23点，每隔3小时触发一次
    - cron: "0 7-23/3 * * *"
  # 手动触发
  workflow_dispatch:
```
