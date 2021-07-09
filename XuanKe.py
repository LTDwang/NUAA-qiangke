# !/usr/bin/env/ python3
# -*- coding : utf-8 -*-
# @Time      :2021/6/20 1:01
# @Author    :Rpeng


import requests
import datetime
import re
import time
from selenium import webdriver


def courseinfo(cookie, id):
    print('正在获取抢课信息！请稍后！')

    # url = 'http://aao-eas.nuaa.edu.cn/eams/stdElectCourse!data.action?profileId=983'
    url = 'http://aao-eas.nuaa.edu.cn/eams/stdElectCourse!data.action?profileId='+id

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'cookie': cookie
    }

    response = requests.get(url, headers = headers)

    find_id = re.compile('id:(\d+),')      # 找课程id的正则表达式
    find_name = re.compile("name:'(.*)',")      # 找课程名称的正则表达式

    id_list = re.findall(find_id, response.text)  # 用来存贮所有的课程的id

    name_list = []   # 用来存储所有的课程名称

    # 课程名称好像不是很会分离出来，所以用的方法复杂了点
    for item in response.text.split('code:'):
        name = re.findall(find_name,item)
        if len(name) != 0:
            name_list.append(name[0])
        else:
            break    # 列表中最后一个元素中没有name


    for i in range(len(id_list)):    # 输出所有信息
        print('序号:',i,'   课程ID：',id_list[i],'   课程名称',name_list[i])

    print('请输入想要抢的课程的序号，（如果输入多个序号，以空格分开）其中课程排序与教务处中的排序相同')
    num = input()
    id_need = []

    for i in num.split(' '):
        id_need.append(id_list[int(i)])

    return id_need    # 返回所有需要抢课的课程id

def qiangke(cookie, num, id):
    time = input('请输入抢课界面开启的时间（格式：2021-06-17 15:59:59）')

    dt = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    # url = 'http://aao-eas.nuaa.edu.cn/eams/stdElectCourse!batchOperator.action?profileId=983'
    url = 'http://aao-eas.nuaa.edu.cn/eams/stdElectCourse!batchOperator.action?profileId='+id

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'cookie': cookie
    }
    form_data_list = []

    for id in num:
        para_1 = id + ':true:0'
        para_2 = id

        form_data = {
            'optype': 'true',
            'operator0': para_1,
            'lesson0': para_2
        }
        form_data_list.append(form_data)      # 所有的课程的post表单


    while 1:
        if datetime.datetime.now() > dt:      # 如果现在的时间大于16：00，学校选课的时间一般是下午16:00
            for data in form_data_list:
                response = requests.post(url, headers=headers, data=data)    # 发送抢课请求
                print(re.findall('([\u4e00-\u9fa5]+)', response.text))    # 打印返回信息中的中文部分，反正一般就是一两句话，选上或者没选上
        else:
            print('抢课是界面未开启，请等待：', dt-datetime.datetime.now())

        time.sleep(0.7)     # 每运行一次，停止0.7s，防止教务处返回“请不要点击过快”

# 由于教务处登录密码进行了加密，本人太菜,不知道怎么登录，只好写一点就放着了
def getcookie():
    opt = webdriver.ChromeOptions()
    opt.headless = True
    browser = webdriver.Chrome(options = opt)
    browser.get('https://authserver.nuaa.edu.cn/authserver/login?service=http%3A%2F%2Faao-eas.nuaa.edu.cn%2Feams%2FlocalLogin.action')
    account = input('请输入统一身份认证的账号：')
    password = input('请输入统一身份认证的密码：')
    browser.find_element_by_xpath('//*[@id="username"]').send_keys(account)
    browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    browser.find_element_by_xpath('//*[@id="login_submit"]').click()

    cookie = ''
    for dic in browser.get_cookies():
        cookie+=dic['name']+'='+dic['value']+';'

    print('登录成功！获取cookies成功！')
    return cookie.strip(';')

def LookUpUrl(cookie):
    pass

def setTime():
    time = input('请输入抢课开始的时间（格式：2021-06-17 16:00:00）:')
    dt = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    return dt

def getid():
    print('''
                           使用须知：
                           
    1,由于每次教务处抢课的网址略有不同，所以在使用本程序之前，请提前登录教务处，
    查看本次抢课的网址，举个栗子：某次抢课的网址为：http://aao-eas.nuaa.edu.cn/eams/stdElectCourse!batchOperator.action?profileId=983
    这个网址已经失效，但是本次抢课的网址大概率只是最后面的id号发生改变，所以请到教务处抢课界面，然后查看浏览器栏的网址，
    输入最后三位数字，本程序会自动修改代码里的那三位数字，保证在正确的网址发起抢课请求
    
    2,本程序使用的是谷歌浏览器90.0.4430.93版本，如果您没有谷歌浏览器，下载一个，Google浏览器yyds！
    
    3，本程序运行时会自动打开一个Google浏览器窗口，您就不要再打开新的浏览器登录了，避免重复登录导致某一方被挤下来，在自动弹出的Google浏览器界面
    操作是不会被挤下来的，可放心使用，保证本程序抢课失败的话，您依旧能手动抢课，节省宝贵的时间
    
    4，一般而言，教务处的时间和您电脑的时间相差2-3min，所以前几分钟抢不到课很正常，您手动抢也是打不开抢课界面的，可以稍微等等
    
    5，本程序设置为0.7s发送一次抢课请求，可自行调整，太快的话会被教务处屏蔽（屏蔽的话也只是返回一句“请不要过快点击”，3s左右就恢复正常了）
    太慢的话抢不到课，您自己看着办~
    
    6，本程序设置的是下午16:00开始抢课（一般都是这个时间抢课，应该不会改变吧）
    
    7，还没想好说啥
    
    ''')
    print('---------------手动分割线--------------')
    id = input('请输入最后三位数字：')
    return id

def main():
    id = getid()
    cookie = getcookie()
    num = courseinfo(cookie,id)    # 得到需要抢课的课程的ID号
    qiangke(cookie, num,id)     # 抢课部分

if __name__ == '__main__':
    main()