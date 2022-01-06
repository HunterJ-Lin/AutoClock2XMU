from selenium import webdriver
from datetime import datetime
import time
import logging
import json
import pytz

#定义邮件功能，发件方以QQ邮箱为例
# intitle, 接收邮件的标题
# intext, 接收邮件的内容
def SendMail(config, intitle, intext):

    from email.mime.text import MIMEText
    from email.header import Header
    from smtplib import SMTP_SSL

    host_server = config['host_server']  # QQ邮箱smtp服务器
    sender_qq = config['sender_qq']  # 发送者QQ
    pwd = config['pwd']  # 密码，通常为授权码
    sender_qq_mail = config['sender_qq_mail']  # 发送者QQ邮箱地址
    username = config['username']
    receiver = config['receiver']

    mail_content = intext + str(get_world_time_now(strftime="%Y-%m-%d %H:%M:%S %Z%z"))
    mail_content += 'Here is the test data, please confirm: \n'
    mail_content += '1> Username:' + username + '\n'
    mail_content += '2> Time:' + str(get_world_time_now(strftime="%Y-%m-%d %H:%M:%S %Z%z")) + '\n'
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

def get_world_time_now(strftime="%H:%M",timezone='Asia/Shanghai'):
    return datetime.fromtimestamp(int(time.time()),pytz.timezone(timezone)).strftime(strftime)


def main():
    with open('config.json','rb') as f: config = json.load(f) 
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    file_handler = logging.FileHandler(config['log_file'],"w", encoding="UTF-8")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    while True:
        try:

            logger.info('当前时间： '+str(get_world_time_now(strftime="%Y-%m-%d %H:%M:%S %Z%z")))
            now = get_world_time_now(strftime="%H:%M")

            if True or (now>='07:00' and now<='09:00'):
                logger.info('---------------------------------------'+'\n')
                logger.info(str(get_world_time_now(strftime="%Y-%m-%d %H:%M:%S %Z%z"))+' 询问打卡'+'\n')
                option = webdriver.ChromeOptions()
                option.add_experimental_option('excludeSwitches', ['enable-automation'])
                # option.add_argument('--headless')
                # option.add_argument('--disable-gpu')
                browser = webdriver.Chrome(executable_path=config['chromedriver'],options=option)
                browser.get('https://xmuxg.xmu.edu.cn/login')

                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="loginLayout"]/div[3]/div[2]/div/button[3]').click()
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="username"]').send_keys(config['username'])
                browser.find_element_by_xpath('//*[@id="password"]').send_keys(config['password'])
                browser.find_element_by_xpath('//*[@id="casLoginForm"]/p[*]/button').click()
                current_window = browser.current_window_handle  # 获取当前窗口handle name
                time.sleep(1)

                #print('cur:',current_window)
                #browser.find_element_by_xpath('//*[@id="mainPage-page"]/div[1]/div[3]/div[2]/div[2]/div[3]/div/div').click()
                #注意学校系统维护，经常会修改css选择器
                browser.find_element_by_css_selector('#mainPage-page > div.v-gm-scrollbar.main-p.gm-autoshow.gm-scrollbar-container > div.gm-scroll-view > div.shadow_box.box_wrap_2 > div.v-gm-scrollbar.gm-autoshow.gm-scrollbar-container > div.gm-scroll-view > div > div:nth-child(2) > div.grow_1.box_flex.column.justify_center > div.text').click()
                
                time.sleep(2)
                all_window=browser.window_handles
                #print('all',all_window)
                for window in all_window:
                    if window != current_window:
                        browser.switch_to.window(window)

                current_window = browser.current_window_handle  # 获取当前窗口handle name
                time.sleep(2)
                browser.find_element_by_xpath('//*[@id="mainM"]/div/div/div/div[1]/div[2]/div/div[3]/div[2]').click()
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="select_1582538939790"]/div/div/span[2]/i').click()
                time.sleep(1)

                if browser.find_element_by_xpath('//*[@id="select_1582538939790"]/div/div/span[1]').get_attribute('innerHTML') == '是 Yes':
                    logger.info('已打过卡'+'\n')
                else:
                    browser.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]/li').click()
                    browser.find_element_by_class_name('form-save').click()
                    alert = browser.switch_to.alert
                    alert.accept()
                    logger.info('成功打卡'+'\n')

                    intitle = 'Successfully clocked again! \n'
                    intext = 'Congratulations, you have successfully clocked in \n'
                    SendMail(config, intitle, intext)

                browser.quit()
                logger.info('---------------------------------------'+'\n')

            else:
                logger.info('++++++'+'\n')
                logger.info('不到打卡时间'+'\n')
                logger.info('++++++'+'\n')

            time.sleep(20*60)  #这里调整检查间隔，此时设置为20分钟一次。

        except Exception as e:

            logger.warning('出现异常')
            if True:
                intitle = 'ERRORS!!! Check it carefully. \n'
                intext = '出现异常:'
                SendMail(config, intitle, intext+str(e))
            logger.warning(e)

            if browser is not None:
                browser.quit()
            time.sleep(60*60) 
        logger.info('\n')

if __name__ == '__main__':
    main()
