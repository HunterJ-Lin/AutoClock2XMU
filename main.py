from selenium import webdriver
import time
import datetime
log = open('./log.txt','a')
username = '' #统一身份用户名
password = ''  #统一身份密码
while True:   
    try:
        log.write('当前时间： '+str(datetime.datetime.now())+'\n')
        now = datetime.datetime.now().strftime("%H:%M")
        if now >='07:00' and now<='12:00':
            log.write('---------------------------------------'+'\n')
            log.write(str(datetime.datetime.now())+' 询问打卡'+'\n')
            option = webdriver.ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.add_argument('--headless')
            option.add_argument('--disable-gpu')
            browser = webdriver.Chrome(executable_path="C:/Program Files/Google/Chrome/Application/chromedriver.exe",options=option)
            browser.get('https://xmuxg.xmu.edu.cn/xmu/login')
            time.sleep(0.1)
            browser.find_element_by_xpath('//*[@id="loginLayout"]/div[3]/div[2]/div/button[2]').click()
            username = ''
            password = ''
            time.sleep(0.1)
            browser.find_element_by_xpath('//*[@id="username"]').send_keys(username)
            browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)
            browser.find_element_by_xpath('//*[@id="casLoginForm"]/p[5]/button').click()
            current_window = browser.current_window_handle  # 获取当前窗口handle name
            time.sleep(0.1)
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
            time.sleep(0.1)
            browser.find_element_by_xpath('//*[@id="select_1582538939790"]/div/div/span[2]/i').click()
            time.sleep(0.2)
            if browser.find_element_by_xpath('//*[@id="select_1582538939790"]/div/div/span[1]').get_attribute('innerHTML') == '是 Yes':
                log.write('已打过卡'+'\n')
            else:
                browser.find_element_by_xpath('//*[@id="select_1582538939790"]/div/div/span[2]/i').click()
                time.sleep(0.2)
                browser.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]/li/label').click()
                time.sleep(0.2)
                browser.find_element_by_xpath('//*[@id="preview1604556559372"]/span/span').click()
                log.write('成功打卡'+'\n')
            browser.quit()
            log.write('---------------------------------------'+'\n')
        time.sleep(5*60)
    except Exception:
        log.write('出现异常'+'\n')
    log.write('\n')
    log.flush()
log.close()
