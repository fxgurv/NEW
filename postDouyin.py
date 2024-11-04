# coding: utf-8
# import os
# import time
# import pandas as pd
from scrap_util import getDriver
import helium as hm
import pickle

# from requests.cookies import RequestsCookieJar
# import pickle
# from selenium.webdriver.common.by import By
# import requests
# from selenium.webdriver.common.keys import Keys


url = 'https://creator.douyin.com/'
movie_path = "./movie_output/"
own_movie_csv = "公告信息_test.csv"    #  -----------------
# 账号cookie存储表达
cookie_f = './cookie_list/{}.pkl'  

# 映射关系，账号名 对应该账号的cookie
#  uv_map = {"zdx":"zdx_1", "zhangzefang": "zhangzefang_1"} 


def get_cookie(fn):
    # 清除浏览器打开已有的cookies
    # browser.delete_all_cookies()  
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
def senDouyin(driver = None, account_name="zdx_1", title='北京市三支一扶公告', movie_path = "./movie_output/a.mp4", loc = "北京"):
    import time
    cookie_local_f = cookie_f.format(account_name)
    local_cookie = get_cookie(cookie_local_f)

    # driver = getDriver()
    hm.set_driver(driver)  # 给它一个selnuim driver
    hm.go_to("www.baidu.com")
    hm.go_to(url)
    # driver.get_screenshot_as_file("1.png")
    # for k,v in s.cookies.items():
    #     driver.add_cookie({'name':k, 'value':v}) 
    for k,v in local_cookie.items():
        driver.add_cookie({'name':k, 'value':v}) 

    hm.go_to(url)

    if hm.Button("开始体验").exists():
        # hm.wait_until(hm.Button("开始体验").exists)
        hm.click(hm.Button("开始体验"))
    if hm.Button("下一步").exists():
        hm.click(hm.Button("下一步"))
        hm.click(hm.Button("完成"))
    time.sleep(1)
    hm.click(hm.Button("发布作品"))
    time.sleep(1)
    hm.drag_file(movie_path, to="或直接将视频文件拖入此区域")

    time.sleep(2)
    if hm.Text("我知道了").exists():
        hm.click(hm.Text("我知道了"))
    time.sleep(1)
    # if hm.Text("我知道了").exists():
    #     hm.click(hm.Text("我知道了"))
    # if hm.Button("我知道了").exists():
    #     hm.click(hm.Button("我知道了"))
    driver.get_screenshot_as_file("e1_wirte_title.png")
    time.sleep(3)
    # 写一个合适的标题，让更多人看到
    driver.find_element_by_class_name("editor-kit-editor-container").click()

    hm.write(title)
    time.sleep(1)
    driver.get_screenshot_as_file("e1_start_choose封面.png")
    if hm.Text("选择封面").exists():
        hm.click(hm.Text("选择封面"))
    if hm.Text("设置封面").exists():
        hm.click("设置封面")
    time.sleep(1)
    if hm.Button("完成").exists():
        hm.click(hm.Button("完成"))
    # if hm.Text("完成").exists:
    #     hm.click(hm.Text("完成"))
    driver.get_screenshot_as_file("e1_完成_choose封面.png")
    time.sleep(1)

    hm.click("输入地理位置")
    time.sleep(1)

    hm.write("北京市")
    time.sleep(1)
    hm.click("北京市")

    driver.find_element_by_class_name("button--1SZwR").click() 
    time.sleep(1)
    driver.get_screenshot_as_file("e1_after_发布.png")
    driver.close()

# 下拉选择第一个 待验证调试
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select

# driver = webdriver.Chrome()

# # Navigate to the webpage with the dropdown menu
# driver.get("https://example.com")

# # Find the dropdown menu element
# dropdown_element = driver.find_element_by_id("myDropdown")

# # Create a Select object from the dropdown element
# dropdown = Select(dropdown_element)

# # Select the first option in the dropdown menu
# dropdown.select_by_index(0)