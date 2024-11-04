# coding: utf-8
import os 
from datetime import datetime
from PIL import Image,ImageFilter,ImageFont,ImageDraw
import matplotlib.pyplot as plt 
import math
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

post_img = "res_post.jpg"   # 底图，确定尺寸


# 最佳实践
# lines = textwrap.wrap(text, width=40)
# y_text = h
# for line in lines:
#     width, height = font.getsize(line)
#     draw.text(((w - width) / 2, y_text), line, font=font, fill=FOREGROUND)
#     y_text += height
    
#  将文字居中显示
def longTextCut(text, line_words):
    """cut the text to len / given_num  lines"""
    total_len = len(text)
    num_line = math.ceil(total_len/line_words)
    num_line = max(num_line, 1)
    res = []
    for i in range(num_line):
        start_inx = int(i*line_words)
        end_inx = int(line_words* (i+1))
        sub_seq = text[start_inx : end_inx]
        res.append(sub_seq)
    lines = textwrap.wrap(text, width=line_words)
    return res
    return lines

# lines = textwrap.wrap(text, width=10)

#  w文字变形，每行不超过多少字，方便阅读
def reshape_texts(lines, line_words):
    new_lines = []
    for it in lines:
        sub_lines = it.split("\n")
        split_lines = []
        for inx, sub_it in enumerate(sub_lines):
            if len(sub_it) > line_words:
                relen_text = longTextCut(sub_it, line_words)
                split_lines.extend(relen_text)
            else:
                split_lines.append(sub_it)
        new_lines.extend(split_lines)
    return new_lines


#  w文字变形，每行不超过多少字，方便阅读
def reshape_texts_end(lines, line_words):
    new_lines = []
    for it in lines:
        sub_lines = it.split("。")
        # t_ = [len(i) for i in sub_lines]
        # y_ = [i > line_words for i in t_]
        split_lines = []
        for inx, sub_it in enumerate(sub_lines):
            if len(sub_it) > line_words:
                relen_text = longTextCut(sub_it, line_words)
                split_lines.extend(relen_text)
            else:
                split_lines.append(sub_it)
        new_lines.extend(split_lines)
    return new_lines




#高斯模糊类
class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"
    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds
    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)

# self.background_url=get_bing_image()
#卡片生成类     16:9
class myPost:
    def __init__(self, front_img=None,
            img = r'./broadcast/kaobianBottem.jpeg'
        ):
        self.frontground = Image.open(front_img) if front_img else None  # bing img 
        #     if type(image) is str:
        #     return image
        # elif type(image) is Image.Image:
        #     return encode_pil_to_base64(image).decode()
        self.img= Image.open(img) if type(img) is str else Image.fromarray(img)  #底稿，确定尺寸
        self.icon=None 
        # self.icon=Image.open(self.icon_url).convert("RGBA")
        #纵向间距
        # self.spacing=spacing
        self.width, self.height=self.img.size

    #加载小图
    def loadIcon(self, point=(50,50)):
        """point=(x,y)"""
        pass
        # self.img.paste(self.icon,point,self.icon)
    def get_width_height(self):
        return self.width,self.height
    
    def getLinesCount(self, sz, spacing):
        words = int(self.width / sz) - 2
        rows = int( self.height / (sz + spacing))
        return (words, rows)

    #高斯模糊图片作为背景
    def drawBlur(self):
        backflur = self.frontground.resize((self.width,self.height), resample=3).filter(MyGaussianBlur(radius=35))
        self.img.paste(backflur,(0, 0))

    #添加前景图片            
    def drawFrontground(self):
        """添加一个前景图壁纸，高斯虚化 
        """
        if not self.frontground:
            return
        x=0
        y=int(self.height*2/3.3)  # 在下半部分画这个图
        srcwidth,srcheight=self.frontground.size
        height=int(srcheight * self.width / srcwidth)
        #重设图片尺寸
        frontground = self.frontground.resize((self.width, height),Image.Resampling.LANCZOS)
        
        alpha_layer = Image.new('L', (self.width, height), 0)
        draw = ImageDraw.Draw(alpha_layer)
        sz = (self.width/2-100, 0, self.width-30, height)
        # print("the area is :", sz)
        draw.ellipse(sz, fill=150)
        self.img.paste(frontground,(x,y),alpha_layer)

    def get_res(self):
        return self.img

    def postTextLine(self, title="Text--test", font="./simsun.ttc", sz=50, x=40, y=90, color = "red"):
        """main title"""
        draw = ImageDraw.Draw(self.img)
        font = ImageFont.truetype(font=font, size=sz)
        draw.text((x,y), title, font=font, fill=color)
        
    def postBoxText(self, texts=["Text--test\n sub text"], font="./simsun.ttc", sz=50, x=40, y=390,
                    color = "red", spacing=40, ali = "left", bac_color=None):
        """lines"""
        # 定义文本内容
        draw = ImageDraw.Draw(self.img)
        font = ImageFont.truetype(font=font, size=sz)
        
        text = "\n".join(texts)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
        
        # 计算文本的宽度和高度
        width = bbox[2] - bbox[0]
        width += int(width * 0.3)
        height = bbox[3] - bbox[1]
        height += int(height * 0.3)
        if bac_color is not None:
            draw.rectangle((x-int(width * 0.15), y-int(height * 0.15), x + width, y + height), fill=bac_color)
        # 计算文本的位置
        # x = (self.width - width) / 2
        # y = (remain_height - height) / 2  # 在剩下的高度中居中显示
        # y = 0 + spacing * 2    #  从头开始展示        
        # 绘制文本
        draw.multiline_text((x, y), text, fill=color, font=font, align=ali, spacing=spacing)

    # 放置文字
    def  postText(self, texts=["Text--test\n sub text"], font="./simsun.ttc", sz=50, x=40, y=390,
                  color = "red", spacing=20):
        draw = ImageDraw.Draw(self.img)
        # Set the font, text contents, and line spacing
        font = ImageFont.truetype(font=font, size=sz)
        # 定义文本内容
        text = "\n".join(texts)
        draw.multiline_text((x, y), text, fill=color, font=font, align="left", spacing=spacing)
        
        # 获取文本的边界框
        # bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)


        # 绘制文本
        # draw.text((x,title_y), title, font=title_front, fill="red")
        # draw.multiline_text((x, y), text, fill=color, font=font, align="left", spacing=spacing)


    def drawCard(self):
        if frontground:
            self.drawFrontground()
        self.postText(title, texts, sz = 40)  
        
    def drawCardExample(self):
        self.drawFrontground()
        self.postTextLine(title="Text--test", font="./simsun.ttc", sz=size, x=40, y=90, color = "red")
        self.postTextLine(title="content of sub text", font="./simsun.ttc", sz=size, x=40, y=90, color = "green")
    def show(self):
        pass

    #保存到本地
    def saveCard(self, path_name):
        save_name =  path_name
        # save_name = str(datetime.today()).split()[0]+'.png'
        self.img.save(save_name)
        return save_name

def generatePost(lines = [""], front_img=None, bac_img="./kaobianBottem.jpeg", fn_name = "test_v1.png"):
    """给定背景，前景，文字，size，生成单张图, 并环肥内存中的图对象"""
    postcard=myPost(front_img=front_img, img = bac_img)
    line_words, rows = postcard.getLinesCount(sz, spacing)
    texts = reshape_texts(lines, line_words)
    print("总行数",len(texts))
    postcard.drawFrontground()
    postcard.postText(texts[0], texts[1:], sz = 40)
    save_name=postcard.saveCard(fn_name)
    # ---opend image
    generated_image = postcard.get_res()
    return generated_image


if __name__ == '__main__':
    # 输入 -========================
    title = "大王叫我来巡山并发布公告，解决就业问题山中有老虎猴子承办问"
    lines = ['四、报名及网上缴费','本次公开考试招聘采取网络报名方式进行，不组织现场报名。报名时间：2023年3月10日至3月17日24:00。',
            '报名网站：广元人事考试网（http://gypta.e21cn.com/）。']
        
    # text = doc['fee_sj']
    # lines = content_with_date(text)  # 只需要有日期信息的字符串
    # texts = "\n".join(lines)
    result_post_file = "post_v1.png"
    bac_img = "./kaobianBottem.jpeg"
    # front_img = "./bingpost/2023-05-13.png"
    bing_post = "bingpost/"
    imgs_ = os.listdir(bing_post)
    imgs_ = [i for i in imgs_ if i.endswith("png")]
    ch_img = random.choice(imgs_)
    front_img = os.path.join(bing_post, ch_img)
    
    postcard=myPost(front_img=front_img, img = bac_img)
    postcard.drawFrontground()
    # 放置标题  + 字体字号
    sz=80
    spacing=20
    words, rows = postcard.getLinesCount(sz=sz, spacing=spacing)
    title_text = longTextCut(title, words)
    title_text = textwrap.wrap(title, width=words)

    print(title_text)
    postcard.postText(title_text, font="./simsun.ttc", sz = sz,
                      x=40, y=150, color = "blue", spacing=20)
            
    sz=50
    spacing=20
    words, rows = postcard.getLinesCount(sz=sz, spacing=spacing)
    texts = longTextCut(lines[1], words)
    print(texts)
    postcard.postText(texts, font="./simsun.ttc", sz = sz,
                      x=40, y=490, color = "green", spacing=spacing)

    
    texts = reshape_texts(lines, words)
    print("texts 长文本 总行数",len(texts))
    postcard.postText([lines[0]],   font="./simsun.ttc", sz = int(sz*1.5),x=40, y=790, color = "red", spacing=spacing)
    postcard.postText(texts,   font="./simsun.ttc", sz = sz,x=40, y=990, color = "green", spacing=spacing)
    save_name=postcard.saveCard(result_post_file)
    print(save_name)
    # postcard.show()

