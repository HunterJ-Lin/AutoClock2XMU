# AutoClock2XMU
厦门大学疫情自动打卡，07:00-11:00，14:00-19:00每20分钟自动轮询打卡情况（可配置

# 注意！！！
打卡是基于学校要求我们每天进行的活动以向学校报告我们的情况。但是由于大多数情况我们都是正常状态。因此这个项目可以帮助我们在正常情况下进行自动打卡确认，减少不必要的重复无意义劳动是本项目的初衷。在出现身体不适时可以通过修改打卡内容来报告非正常情况，希望此项目能够在你如实汇报内容的情况下带来便利。

# 环境要求
windows、python、selenium（需要配置chromedriver驱动，目前仅支持chrome浏览器，最好禁止chrome浏览器更新，否则需要频繁更换对应版本的chromedriver驱动）、根据自己的统一身份认证，qq邮箱配置config.json
{
    "username" : "", 
    "password" : "", 
    "receiver" : "", 
    "host_server" : "",  
    "sender_qq" : "",  
    "pwd" : "",  
    "sender_qq_mail" : "",
    "log_file" : "./log.txt",
    "chromedriver" : "C:/Program Files/Google/Chrome/Application/chromedriver.exe",
    "comment" : "username -> 统一身份用户名, password -> 统一身份密码, receiver -> 接收打卡信息的邮箱, host_server -> QQ邮箱smtp服务器, sender_qq -> 发送者QQ, pwd -> qq邮箱授权码, sender_qq_mail -> 发送者QQ邮箱地址, chromedriver -> chrome驱动程序路径, log_file -> log文件"
}

# 使用方法
1、双击start_hidden.vbs(一次，不然会开启多个后台进程)

2、双击stop_all_python.bat(注意！！！会杀死所有python进程)

3、log.txt可以查看打卡情况

4、注意查收邮件即可了解打卡状态
