# 定时获取拷贝漫画更新

[![check](https://github.com/caolib/check-manga-update/actions/workflows/check_update.yml/badge.svg)](https://github.com/caolib/check-manga-update/actions/workflows/check_update.yml)
![GitHub last commit](https://img.shields.io/github/last-commit/caolib/check-manga-update?logo=github)
![GitHub Release](https://img.shields.io/github/v/release/caolib/check-manga-update?link=https%3A%2F%2Fgithub.com%2Fcaolib%2Fcheck-manga-update%2Freleases)
![GitHub License](https://img.shields.io/github/license/caolib/check-manga-update)

## 简介

使用`Github Actions`定期执行python脚本检查个人书架的漫画是否更新，并使用邮件进行通知

## 怎么使用

### 开启邮件SMTP服务

> 此处使用QQ邮箱，可以参阅[邮箱开启SMTP服务](https://clb.pages.dev/2024/12/27/开启SMTP服务/)获取邮箱授权码，这个授权码后面要使用 *暂时还没有测试其他邮箱怎么用:(*

### clone或fork

> 仓库中的`comics.json`文件保存了你的书架中最近更新的漫画(上限20个)：
>
> - 如果你介意别人会看到你的个人书架，你可以**clone**本仓库到本地(~~来，让我看看~~)，然后再推送到你github的私人仓库中 **[private]**
>
> - 如果你不介意别的话，可以直接**fork**本仓库(~~我根本不介意的~~) **[public]**

### 添加Secrets

1. 进入你的仓库，点击**Settings**

![image-20241228123435863](https://s2.loli.net/2024/12/28/y2YDdAGHhiW3Bkg.png)

2. 在左侧栏找到Secrets下的actions，添加图中6个变量，下面有拷贝漫画的token的获取步骤,其他属性按自己的填就行:)

![image-20241228123648544](https://s2.loli.net/2024/12/28/CkFaXtLTQbRU5he.png)

> TOKEN	   拷贝漫画的token
> USERNAME	拷贝 用户名 
> PASSWORD	拷贝 密码
> FROM_EMAIL      发件人邮箱
> TO_EMAIL	收件人邮箱 *可以发给自己:)*
> EMAIL_TOKEN     邮箱授权码

快捷复制:)

```txt
TOKEN
```

```txt
USERNAME
```

```txt
PASSWORD
```

```txt
FROM_EMAIL
```

```txt
TO_EMAIL
```

```txt
EMAIL_TOKEN
```

获取拷贝漫画的token：

- 前往[拷貝漫畫](https://www.mangacopy.com/)，登陆你的账号

- 按F12 或 右键选择**检查** 打开开发者工具

- 打开应用程序一栏，在左侧找到Cookie，复制token的值

  ![image-20241228124951850](https://s2.loli.net/2024/12/28/un3kYgVO5BENLvF.png)

- 仓库中有一个`login.py`文件，可以很方便的获取token，但是会导致你的网站需要重新登陆，所以还是推荐上面的办法获取token（悲

### 测试

你可以手动触发工作流检查是否能正常运作

![image-20241228125755361](https://s2.loli.net/2024/12/28/gIL9aZP3bRcX6N2.png)

邮件提醒示例：

![image-20241228101807069](https://s2.loli.net/2024/12/28/QAyn9otF82c3zfO.png)

## 其他配置

### 修改触发条件

> 触发条件默认是 7点-23点，每隔2小时触发一次，你可以调整触发频率或时间段，例如：
>
> `- cron: "0 7-23 * * *"` : 7-23 每小时触发一次

```yml
on:
  # 定时触发
  schedule:
    # 7点-23点，每隔2小时触发一次
    - cron: "0 7-23/2 * * *"
  # 允许手动触发
  workflow_dispatch:
```

## 计划

- [ ] 可以使用其他邮箱服务
- [ ] 项目文件结构优化，抽取函数到多个py文件

如果对你有帮助的话，不妨给个star⭐
