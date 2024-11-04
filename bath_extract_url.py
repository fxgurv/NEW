# coding: utf-8
# !python scrap_util.py  
from scrap_util import getDriver, titleLocInfo, find_key_paragrap, extract_from_driver, table_record_doc
import helium as hm
import time
import datetime
import numpy as np
import pandas as pd

print("please input the url list to dealt with")
print("调用 web tool TO get Info and context")
urls = ['http://csglw.beijing.gov.cn/zwxx/rsgl/gwygl/202209/t20220909_2812285.html',
 'http://ghzrzyw.beijing.gov.cn/zhengwuxinxi/rsxx/sj/202304/t20230418_3058292.html',
 'http://mzj.beijing.gov.cn/art/2022/6/16/art_383_630732.html',
 'http://www.scrsw.net/zhaokao/2023/zk91559_1.html',
 'https://www.gyct.com.cn/info/1487/112938.htm',
 'http://www.scrsw.net/zhaokao/2023/zk92498_1.html',
 'http://www.hnrs.com.cn/shiye/5148.html',
 'http://www.hnrs.com.cn/shiye/5077.html',
 'http://www.hnrs.com.cn/shiye/5072.html',
 'http://hrss.gd.gov.cn/zwgk/xxgkml/content/post_4148656.html',
 'https://www.gdzz.gov.cn/tzgg/content/post_18310.html',
 'https://www.gdzz.gov.cn/tzgg/content/post_18035.html',
 'https://www.jsdzj.gov.cn/art/2023/2/24/art_28_15933.html',
 'http://www.js.msa.gov.cn/art/2023/2/24/art_11436_1391666.html',
 'http://www.jsrsks.com/index/article/content/id/3315.shtml']
# urls = urls[:2]
num_urls = len(urls)
print(f"需要处理的任务url个数{num_urls}")


st = time.time()

driver = getDriver()
hm.set_driver(driver)  # 给它一个selnuim driver

# 一方面
task_docs = []
contents = []
for task_link in urls:
    hm.go_to(task_link)
    time.sleep(1)
    # driver.get_screenshot_as_file("1.png")
    # html = driver.page_source
    # soup = BeautifulSoup(html, "html.parser")
    items_ = driver.find_elements_by_xpath("//p")
    items_ = [i.text for i in items_ if i.text != ""]
    context_to_label =  "\n".join(items_)
    doc = extract_from_driver(driver)    
    # bm_sj = content_with_date(doc["bm_sj"])
    # fee_sj = content_with_date(doc["fee_sj"])
    # ks_sj = content_with_date(doc["ks_sj"])
    # zkz_sj = content_with_date(doc["zkz_sj"])
    # doc["tidy_bm_sj"] = bm_sj
    # doc["tidy_fee_sj"] = fee_sj
    # doc["tidy_ks_sj"] = ks_sj
    # doc["tidy_zkz_sj"] = zkz_sj
    doc_row = table_record_doc(doc)
    content = [task_link]
    content.extend(doc_row)
    content.append(context_to_label)
    contents.append(content)
    task_docs.append(doc)
    print(doc)
    # save current doc to file
    title = doc["title"].replace("\n", "").strip(" ")
    # fn_name = datetime.datetime.
    # with open("") as f: f.write(jsonfy(doc))
    # mydriver.driver.

driver.close()
print(f"当前任务爬取完成！，总共{num_urls}")

name = ["sub_url", "title", "zwk_year", "zwk_sheng", "zwk_diqu", "zwk_zip", "zwlx", 
            "bm_sj", "fee_sj", "ks_sj",  "zkz_sj",
        "tidy_bm_sj","tidy_fee_sj", "tidy_ks_sj", "tidy_zkz_sj",
        "fn_list", "content"]


end_time = time.time()
cost = end_time - st
print(f"total cost time:{cost}")
# 使用当前时间作为任务标记
dt, tm = str(datetime.datetime.today()).split()
tm = tm[:5]
time_ckt = dt+"_"+tm
fn_name = "./scrap_data/" + time_ckt + ".csv"
df = pd.DataFrame(data=contents, columns=name)
for i in df.columns:
    if np.all(pd.notnull(df[i])) == False:
        df[i].fillna("", inplace=True)
num_res = df.shape[0]
print(f"抓取结果数{num_res}")
df.to_csv(fn_name, index=False)

# TODO 信息数据库保存
print(f"# 信息数据库保存!  在文件中:{fn_name}")
