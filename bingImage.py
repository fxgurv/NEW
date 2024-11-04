# coding: utf-8
import requests,json,re,io,time,hmac,hashlib,base64,random
from urllib.request import urlopen
from datetime import datetime
from PIL import Image,ImageFilter,ImageFont,ImageDraw
from bs4 import BeautifulSoup
import parsel
from faker import Faker
import datetime

print("-------")
def get_bing_image():
    uas = Faker()
    ua=uas.user_agent()
    headers = {'user-agent': ua}
    url = 'https://cn.bing.com'
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    sel = parsel.Selector(res.text, base_url=url)
    # print(sel.css('#preloadBg::attr(href)'))
    url =  sel.css('#preloadBg::attr(href)').extract_first()
    image_bytes = urlopen(url).read()
    data_stream = io.BytesIO(image_bytes)
    # Image.open(data_stream)
    return data_stream

background_rb=get_bing_image()
background=Image.open(background_rb)
path = "bingpost/"
import os 
if not os.path.exists(path):
    os.mkdir(path)
save_name = str(datetime.datetime.today()).split()[0]+'.png'
save_name = path + save_name
background.save(save_name)


