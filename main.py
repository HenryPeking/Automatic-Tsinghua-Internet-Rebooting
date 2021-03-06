#coding:utf-8
__author__ = 'zcy'
#modifier dcl
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests

username_str = "" #用户名
password_str = "" #密码
#Login 代码原理，模拟一个打开Firefox，输入用户名、密码并点击连接的过程
class Login:
    def login(self):
        try:
            driver = webdriver.Firefox()
            driver.get("https://auth4.tsinghua.edu.cn/srun_portal_pc.php?ac_id=163&")
            time.sleep(3)
            username_input = driver.find_element_by_id("username")
            password_input = driver.find_element_by_id("password")
            login_button = driver.find_element_by_id("connect")

            username_input.send_keys(username_str)
            password_input.send_keys(password_str)
            login_button.click()
        except:
            print(self.getCurrentTime(), u"登陆函数异常")
        finally:
            driver.close()


    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    #判断当前是否可以连网
    def canConnect(self):
        try:
            baidu_request=requests.get("http://www.baidu.com")
            if(baidu_request.status_code==200):
                baidu_request.encoding = 'utf-8'
                baidu_request_bsObj = BeautifulSoup(baidu_request.text, 'html.parser')
                baidu_input = baidu_request_bsObj.find(value="百度一下")
                if baidu_input==None:
                    return False
                return True
            else:
                return False
        except:
            print ('error')

    #主函数
    def main(self):
        print (self.getCurrentTime(), u"Hi，自动登陆脚本正在运行")
        while True:
            while True:
                can_connect = self.canConnect()
                if not can_connect:
                    print (self.getCurrentTime(),u"断网了...")
                    try:
                        self.login()
                    except:
                        print(self.getCurrentTime(), u"浏览器出了bug")
                    finally:
                        time.sleep(2)
                        if self.canConnect():
                            print(self.getCurrentTime(), u"重新登陆成功")
                        else:
                            print(self.getCurrentTime(), u"登陆失败，再来一次")
                else:
                    print (self.getCurrentTime(), u"一切正常...")
                    time.sleep(600) #每十分钟检查一次是否掉线
                time.sleep(1)
            time.sleep(self.every)

login = Login()
login.main()
