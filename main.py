from selenium import webdriver
import time
import datetime
import sys

username = '*********' #统一身份用户名
password = '*********' #统一身份密码
receiver = '*********' #接收打卡信息的邮箱

#定义邮件功能，发件方以QQ邮箱为例，这里定义了四个参数分别为：
# 1> username, 用户名。用作测试
# 2> receiver, 接收邮件的地址。作用测试
# 3> intitle, 接收邮件的标题
# 4> intext, 接收邮件的内容
def SendMail(username, receiver, intitle, intext):

    from email.mime.text import MIMEText
    from email.header import Header
    from smtplib import SMTP_SSL

    host_server = 'smtp.qq.com'  # QQ邮箱smtp服务器
    sender_qq = '*************'  # 发送者QQ
    pwd = '*******************'  # 密码，通常为授权码
    sender_qq_mail = '********'  # 发送者QQ邮箱地址

    mail_content = intext + str(datetime.datetime.now())
    mail_content += 'Here is the test data, please confirm: \n'
    mail_content += '1> Username:' + username + '\n'
    mail_content += '2> Time:' + str(datetime.datetime.now()) + '\n'
    mail_content += '3> Your Email:' + receiver + '\n'
    mail_content += '4> Host Email:' + sender_qq + '\n'
    mail_title = intitle

    smtp = SMTP_SSL(host_server)
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()


while True:

    log = open(sys.argv[0].split('.')[0]+'.txt','a')

    try:

        print('当前时间： '+str(datetime.datetime.now()))
        log.write('当前时间： '+str(datetime.datetime.now())+'\n')
        now = datetime.datetime.now().strftime("%H:%M")

        # 这里把时间分成两部分，第一部分主要为打卡，第二部分为检查
        if (now>='07:00' and now<='11:00') or (now>='14:00' and now<='19:00'):

            log.write('---------------------------------------'+'\n')
            log.write(str(datetime.datetime.now())+' 询问打卡'+'\n')
            option = webdriver.ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.add_argument('--headless')
            option.add_argument('--disable-gpu')
            browser = webdriver.Chrome(executable_path="/home/kick/Soft/chromedriver",options=option) #配置webdriver
            browser.get('https://xmuxg.xmu.edu.cn/login')

            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="loginLayout"]/div[3]/div[2]/div/button[2]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="username"]').send_keys(username)
            browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)
            browser.find_element_by_xpath('//*[@id="casLoginForm"]/p[*]/button').click()
            current_window = browser.current_window_handle  # 获取当前窗口handle name
            time.sleep(1)

            #print('cur:',current_window)
            browser.find_element_by_xpath('//*[@id="mainPage-page"]/div[1]/div[3]/div[2]/div[2]/div[3]/div/div[1]').click()
            time.sleep(2)
            all_window=browser.window_handles
            #print('all',all_window)
            for window in all_window:
                if window != current_window:
                    browser.switch_to.window(window)

            current_window = browser.current_window_handle  # 获取当前窗口handle name
            browser.find_element_by_xpath('//*[@id="mainM"]/div/div/div/div[1]/div[2]/div/div[3]/div[2]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="select_1582538939790"]/div/div/span[2]/i').click()
            time.sleep(1)

            if browser.find_element_by_xpath('//*[@id="select_1582538939790"]/div/div/span[1]').get_attribute('innerHTML') == '是 Yes':
                log.write('已打过卡'+'\n')

                if now>='17:00' and now<='17:30':

                    intitle = 'Check mail, today is OK! \n'
                    intext = 'Check again whether to check in \n'
                    SendMail(username, receiver, intitle, intext)

            else:

                browser.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]/li').click()
                browser.find_element_by_class_name('form-save').click()
                alert = browser.switch_to.alert
                alert.accept()
                log.write('成功打卡'+'\n')

                intitle = 'Successfully clocked again! \n'
                intext = 'Congratulations, you have successfully clocked in \n'
                SendMail(username, receiver, intitle, intext)

            browser.quit()
            log.write('---------------------------------------'+'\n')

        else:

            log.write('++++++'+'\n')
            log.write('不到打卡时间'+'\n')
            log.write('++++++'+'\n')

        time.sleep(30*60)  #这里调整检查间隔，此时设置为30分钟一次。

    except Exception:

        log.write('出现异常'+'\n')
        browser.quit()

        if now>='17:00' and now<='17:30':

            intitle = 'ERRORS!!! Check it carefully. \n'
            intext = 'ERRORS!!! ERRORS!!! please clock-in by yourself first and contact *****\n'
            SendMail(username, receiver, intitle, intext)

    log.write('\n')
    log.close()
