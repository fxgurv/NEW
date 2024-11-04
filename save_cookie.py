# coding: utf-8
import helium as hm
import os
import pandas as pd
import pickle
from scrap_util import getDriver


url = 'https://creator.douyin.com/'
# 账号cookie存储表达
cookie_f = './cookie_list/{}.pkl'  


def save_cookie(driver, fn):
    '''
    说明：pickle库来序列化数据(把格式数据存入文件和加载到内存)
    '''
    cookies = driver.get_cookies()
    cookies1={}
    for i in cookies:
        cookies1[i["name"]]=i["value"]    
    # cookies = browser.get_cookies()
    # 方法一
    # with open('taobao_cookie.pickle','wb') as f:
    #    pickle.dump(cookies, f)    
    # 方法二
    pickle.dump(cookies1, open(fn,'wb'))


def get_cookie(fn):
    # 清除浏览器打开已有的cookies
    # browser.delete_all_cookies()
    # 方法一
    # with open('taobao_cookie','rb') as f:
    #     cookies = pickle.load(f)
    # for cookie in cookies:
    #     if 'expiry' in cookie:
    #         del cookie['expiry']
    #     browser.add_cookie(cookie)    
    # 方法二
    cookies = pickle.load(open(fn, "rb"))
    new_cookie = {}
    for cookie in cookies: 
        if 'expiry' in cookie:
            continue
        # if isinstance(cookie.get('expiry'), float):
        #     cookie['expiry'] = int(cookie['expiry'])
        new_cookie[cookie] = cookies[cookie]
        # browser.add_cookie(cookie)
    return new_cookie



# ----- ready gogogogo ~ --------------
# ----- ready gogogogo ~ --------------
cookie_fns = ["抖音北京人事考试","抖音广东人事考试","抖音四川人事考试","抖音浙江人事考试","抖音江苏人事考试","抖音山东人事考试","抖音河南人事考试"]

cookie_zdx_f = cookie_f.format(cookie_fns[0])

# driver = getDriver()
# hm.set_driver(driver)  # 给它一个selnuim driver
# hm.go_to(url)
# # driver.get_screenshot_as_file("1.png")
# print("-------------------请扫描二维码登录抖音创作者中心-------------------")
# # TODO & 可视化出二维码 --------------
# hm.click(hm.Text("登录"))
# time.sleep(1)
# hm.click(hm.Text("确认"))
# time.sleep(1)
# qr_element = driver.find_element_by_class_name("qrcode-image")
# qr_element.click()
# qr_element.screenshot("qr.png")


# qr_element = driver.find_element_by_class_name("qrcode-image")
# qr_element.click()
# time.sleep(1)
# qr_element.screenshot("qr.png")
# ipd.Image("qr.png")

# # save and load cookie ways~
# save_cookie(driver, zdx_cookie)
# # 映射关系，账号名 对应该账号的cookie
# #  uv_map = {"zdx":"zdx_1", "zhangzefang": "zhangzefang_1"} 

# # =======================
# # 获取登陆者信息，账号ID/ 开发者id/ 名字/ 手机号/



