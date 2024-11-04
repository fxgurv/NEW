from faker import Faker
import pandas as pd
import re
import sys
import json
import unicodedata
from bs4 import BeautifulSoup  #解析requests请求到的HTML页面
from urllib.parse import urljoin
import cpca  # 地点 city mapping

from selenium import webdriver
import helium as hm
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from keywordInfo import key_pat, zwlx_list

# 北京市信息发布，考编公告~ A  _1 
sub_url ="http://www.beijing.gov.cn/gongkai/rsxx/gwyzk/202211/t20221120_2862819.html"
sub_url ="https://www.js.msa.gov.cn/art/2023/2/24/art_11436_1391666.html"


def getDriver():
    # Set path Selenium
    uas = Faker()
    CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
    CHROMEDRIVER_PATH = './chromedriver'        
    s = Service(CHROMEDRIVER_PATH)
    WINDOW_SIZE = "1920,1080"
    # Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-gpu')
    # 增加一个参数设置
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument(f'user-agent={uas.chrome()}')
    with open('./stealth.min.js') as f:  
        js = f.read()  
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js })
    return driver

def content_with_date(lines):
    if len(lines) < 1:
        return []
    date_pattern1 = r'\d{1,2}月\d{1,2}日'
    date_pattern2 = r'[上|下]午'
    date_pattern3 = r'\d{4}年\d{1,2}月\d{1,2}日'
    inx_ = len(lines)-1
    for inx_, line in enumerate(lines):
        matches = re.findall(f'({date_pattern1}|{date_pattern3})', line)
        if len(matches)>0:
            break
    if len(matches)<1:
        return []
    # new_ = "\n".join(lines[:inx_+1])
    # year_pattern = r'\d{4}年'
    # matches = re.findall(f'({year_pattern})', old_title)
    return lines[:inx_+1]


#👏👏👏 这里需要调整获取多少段落，不至于获得太多冗余信息
def find_key_paragrap(search_text, paragraphs):
    # Loop through the paragraphs and print the text content of those that contain the search text
    for inx_, paragraph in enumerate(paragraphs):
        text = paragraph.text
        if search_text in text:
            # Get the index of the matched line
            # index = text.index(search_text)
            index = inx_
            # Print the matched line and 5 lines before and after it
            start = max(0, inx_)
            end = min(len(paragraphs), index + 7)
            target_paragrap = paragraphs[start:end]
            texts = [i.text for i in target_paragrap]
            dt_lines = content_with_date(texts)
            if len(dt_lines) >= 1:
                return texts
    return None

def titleLocInfo(title):
    """get loction and year from title"""
    # print(title)
    # print(driver.current_url)
    # zwk_year
    year_pattern = r'\d{4}年'
    matches = re.findall(f'({year_pattern})', title)
    zwk_year = matches[0] if len(matches) else "2023" 
    # zwk_sheng
    area_df = cpca.transform([title])
    # 省份
    zwk_sheng = list(area_df["省"])[0] if area_df.shape[0] > 0 else ""
    a_ = list(area_df["市"])[0] if area_df.shape[0] > 0 else ""
    b_ = list(area_df["区"])[0] if area_df.shape[0] > 0 else ""
    zwk_diqu = a_
    # 唯一标识
    zwk_zip = list(area_df["adcode"])[0] if area_df.shape[0] > 0 else ""

    zwlx = zwlx_list[0]   # 默认类型公务员
    for i in zwlx_list:
        if i in title:
            zwlx = i
    res = [zwk_year, zwk_sheng, zwk_diqu, zwk_zip, zwlx]
    # print("\t".join(res))
    return res

def extract_from_driver(driver):
    """ get result from url request BeautifulSoup(texts,'html.parser')
    return: doc_item ,time source info, and attach information
    """
    title=driver.title
    #[zwk_year, zwk_sheng, zwk_diqu, zwk_zip, zwlx]
    title_info = titleLocInfo(title)

    items_ = driver.find_elements_by_xpath("//p")
    items_ = [i.text for i in items_ if i.text != ""]
    context_to_label =  "\n".join(items_)

    paragraphs = driver.find_elements_by_tag_name("p")
    paragraphs = [i for i in paragraphs if i.text.strip() != ""]

    # extract keyword info
    # key_pat["报名"],     key_pat["考试"],    key_pat["缴费"],    key_pat["准考证"],    key_pat["all"] 
    def get_key_info(pt:list):
        for item in pt:
            res_ = find_key_paragrap(item, paragraphs)
            if res_ is not None:
                return res_
        return ""
    bm_sj = get_key_info(key_pat["报名"])
    fee_sj = get_key_info(key_pat["缴费"])
    ks_sj = get_key_info(key_pat["考试"])
    zkz_sj = get_key_info(key_pat["准考证"])    
    # 附件 links  ".doc" or ".xls" ".xlsx"
    links = driver.find_elements_by_tag_name("a")
    unique_link = {}
    for link in links:
        url_ = link.get_attribute("href")
        content_ = link.get_attribute("textContent")
        url_con = url_ and (url_.endswith(".doc") or url_.endswith(".xls") or url_.endswith(".xlsx"))
        name_con = content_ and (content_.endswith(".doc") or content_.endswith(".xls") or content_.endswith(".xlsx"))
        if  url_con or name_con:
            unique_link[content_] = url_
    name = ["title", "zwk_year", "zwk_sheng", "zwk_diqu", "zwk_zip", "zwlx", 
                "bm_sj", "fee_sj", "ks_sj",  "zkz_sj",
            "fn_list" ,
            "tidy_bm_sj","tidy_fee_sj", "tidy_ks_sj", "tidy_zkz_sj"
           ]
    doc_item = [title]
    doc_item.extend(title_info)    
    doc_item.extend([bm_sj, fee_sj, ks_sj, zkz_sj,
                unique_link])
    td_bm_sj = content_with_date(bm_sj)
    td_fee_sj = content_with_date(fee_sj)
    td_ks_sj = content_with_date(ks_sj)
    td_zkz_sj = content_with_date(zkz_sj)
    doc_item.extend([td_bm_sj, td_fee_sj, td_ks_sj, td_zkz_sj])
    doc_dc = {}
    for k_, v_ in  zip(name,  doc_item):
        doc_dc[k_] = v_
    return doc_dc

# 用于表格化记录
def table_record_doc(doc):
    fn_dc = doc["fn_list"]
    row_item = [
        doc["title"], doc["zwk_year"], doc["zwk_sheng"], doc["zwk_diqu"], doc["zwk_zip"], 
        doc["zwlx"], 
        "\n".join(doc["bm_sj"]),
        "\n".join(doc["fee_sj"]),
        "\n".join(doc["ks_sj"]),
        "\n".join(doc["zkz_sj"]),
        "\n".join(doc["tidy_bm_sj"]),
        "\n".join(doc["tidy_fee_sj"]),
        "\n".join(doc["tidy_ks_sj"]),
        "\n".join(doc["tidy_zkz_sj"]),
        "\n".join([f"{k}:{v}" for k,v in fn_dc.items()])
    ]
    name = ["title", "zwk_year", "zwk_sheng", "zwk_diqu", "zwk_zip", "zwlx", 
                "bm_sj", "fee_sj", "ks_sj",  "zkz_sj",
            "tidy_bm_sj","tidy_fee_sj", "tidy_ks_sj", "tidy_zkz_sj",
            "fn_list"]
    a = pd.DataFrame(data=[row_item], columns=name)
    return row_item

if __name__ == '__main__':
    mydriver = getDriver()
    # hm.goto(url)
    url = "https://www.js.msa.gov.cn/art/2023/2/24/art_11436_1391666.html"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    hm.set_driver(mydriver)  # 给它一个selnuim driver
    hm.go_to(sub_url)
    # mydriver.driver.
    import time
    time.sleep(2)
    res = extract_from_driver(mydriver)
    print("-raw, mostly contains----------------------------")
    print(res)
    print("报名，缴费，考试，准考证最相关信息")
    bm_sj = doc["bm_sj"]
    bm_sj = content_with_date(bm_sj)
    fee_sj = content_with_date(doc["fee_sj"])
    ks_sj = content_with_date(doc["ks_sj"])
    zkz_sj = content_with_date(doc["zkz_sj"])
    print(bm_sj)
    print(fee_sj)
    print(ks_sj)
    print(zkz_sj)
    mydriver.close()
    