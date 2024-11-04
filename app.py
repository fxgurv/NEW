import time
import random
import os
import gradio as gr
import pandas as pd
import textwrap

import traceback

# Crawler-------------
from save_cookie import save_cookie, get_cookie, cookie_f
from scrap_util import getDriver, titleLocInfo, find_key_paragrap, extract_from_driver, table_record_doc
import helium as hm
from postDouyin import senDouyin
# Model-------------
from transformers import *

import pandas as pd
import os
import random
import IPython.display as ipd
import numpy as np
# Video-------------
import moviepy.video.io.ImageSequenceClip
from moviepy.editor import AudioFileClip,TextClip,CompositeVideoClip

import inspect, math
from PIL import Image, ImageDraw, ImageFont
from txtImgPost import  myPost, reshape_texts, generatePost
# Publish-------------


VIPtitle = "👑Content Input to Video Generation✍️👒"
print(f"&gt;&gt;&gt;{VIPtitle}")
print(f"Secret Key File Path:{cookie_f}")
mv_path = "./movie_output"
img_path = "./imgpost"
font_path = "./fonts"
movies = [os.path.join(mv_path,i) for i in os.listdir(mv_path) if i.endswith("mp4")]
exam_video = movies[0]
imgs_cur = [os.path.join(img_path,i) for i in os.listdir(mv_path) if i.endswith("png")]
templates_path = "./templates/"
templates = [os.path.join(templates_path,i) for i in os.listdir(templates_path) if i.endswith("csv")]
templates_name = [i.strip(templates_path).strip(".csv") for i in templates]
preview_templates = [os.path.join(templates_path,i) for i in os.listdir(templates_path) if i.endswith("jpg")]
# Font------
font_list = [os.path.join(font_path,i) for i in os.listdir(font_path) if i.split(".")[1] in ["ttc",  "ttf", "otf"]]
background_img = "kaobianBottem.jpeg"
background_img = "./templates/zf_board_temp.jpeg"

a_ = Image.open(background_img)
WIDTH = 900
HEIGHT = 1400
WIDTH,HEIGHT = a_.size

should load from files and build new from file
cookie_fns = ["Douyin Beijing Personnel Examination","Douyin Guangdong Personnel Examination","Douyin Sichuan Personnel Examination","Douyin Zhejiang Personnel Examination","Douyin Jiangsu Personnel Examination","Douyin Shandong Personnel Examination","Douyin Henan Personnel Examination"]
cookie_fns = os.listdir("./cookie_list/")
cookie_fn = cookie_fns[0]
description = "URL--&gt; Crawl--&gt;Parse--&gt; Audio--&gt; Image--&gt; Video"

driver = getDriver()
sub_url ="https://www.js.msa.gov.cn/art/2023/2/24/art_11436_1391666.html"
hm.set_driver(driver)  # Give it a selnuim driver
hm.go_to(sub_url)
html = driver.page_source
html = ""

examples = [
    ["Chaoyang District 2023 First Half of the Year Public Examination and Recruitment of Personnel for Public Institutions Announcement - \"Sichuan•Chaoyang\" Portal",
     "Registration Time. This public examination and recruitment will be conducted through online registration and no on-site registration will be organized. Registration time: March 10, 2023 to March 17, 2023, 24:00. Registration Website: Guangyuan Personnel Examination Website (http://gypta.e21cn.com/)",
     "Payment Time. May 27, 2023, Online Payment",
     "Examination Time - Written Examination Time 2. The written examinations will be held on April 8 and 9, 2023 (specific time and location are subject to the Admission Ticket). Among them, the subject of the written examination on April 8 is \"Education Public Foundation\", and the subjects of the written examination on April 9 are \"Public Subject Written Examination for Health Professional and Technical Personnel\" and \"Comprehensive Knowledge\"",
     "Admission Ticket Collection. Candidates who have successfully registered and paid online can print their admission ticket by logging into the registration website before 24:00 on April 3 to April 7, 2023, using their ID number and name"
    ],
    ]

# Prediction function
qa = pipeline("question-answering", model="uer/roberta-base-chinese-extractive-qa")
def custom_predict(context, question):
    answer_result = qa(context=context, question=question)
    answer = question + ": " + answer_result["answer"]
    score = answer_result["score"]
    return answer, score

def image_preview(orimage=None, text="Hello Ai", x=10, y=20, w=500, h=100, bac_color = "#FFbbFF",
                  txt_color = "#000000",front="simsun.ttc", size = 50):
    if orimage is None:
        return None
    size = int(size)
    image = Image.fromarray(orimage)
    draw = ImageDraw.Draw(image)
    draw.rectangle((x, y, x + w, y + h), fill=bac_color)
    # Add text to the text box
    font = ImageFont.truetype(front, size)
    text_x = x + size
    text_y = y + size
    words_perline = int(w / size)
    draw.text((text_x, text_y), text, font=font, fill=txt_color)
    return image

# Location temporarily determined by the system
def generate_image(bac_img, title,a,b,c,d,e,f,   #-- Current number of characters in the text line can be adjusted, width can be adjusted words_curline or text width
                   font_title, sz1, title_x, title_y, color1,   # for title
                   font_subtt, sz2, subtt_x, subtt_y, color2,
                   font_txt,   sz3, txt_x,  color3, bac_color):
    if bac_img is None:
        bac_img = "./kaobianBottem.jpeg"
    bing_post = "bingpost/"
    spacing = 20
    imgs_ = os.listdir(bing_post)
    imgs_ = [i for i in imgs_ if i.endswith("png")]
    ch_img = random.choice(imgs_)
    front_img = os.path.join(bing_post, ch_img)    
    front_img = None      
    postcard=myPost(front_img=front_img, img = bac_img)
    width, height = postcard.get_width_height()
    print(f"width, height :{width}  {height}")
    #  Foreground image, parameters to be opened for control
    postcard.drawFrontground() 
    # Place the title  + font size
    spacing=20
    # --Ideal total number of characters per line
    words, rows = postcard.getLinesCount(sz=sz1, spacing=spacing) 
    words = (width - title_x) / ( sz1 + spacing) 
    words = int(words) + 1
    title_text = textwrap.wrap(title, width=words)
    title_text = [i.center(words) for i in title_text]
    postcard.postBoxText(title_text, font=font_title, sz = sz1,
                      x=title_x, 
                          # x=0, 
                     y=title_y, color = color1, spacing=spacing,  ali = "center",
                         bac_color=None)

    # Subtitle + content processing  + number of characters per line
    # x=40
    y = subtt_y  #  Title and remaining content height
    #- -- Deduct the starting position, the number of characters that can be placed ---
    words = int((width) / sz3)
    for k,contents in enumerate([a,b,c,d,e,f]):
        if len(contents) < 1:
            continue
        lines = contents.split("。")
        if len(lines) < 2:
            continue
        sub_title = lines[0]
        sub_texts = "。".join(lines[1:])
        words = int((width - txt_x) / sz3) - 2
        sub_text = textwrap.wrap(sub_texts, width=words)
        sub_text = [i.center(words) for i in sub_text]
        # -----Text box effect--------
        draw.rectangle((x, y, x + w, y + h), fill=bac_color)
        postcard.postBoxText([sub_title], font=font_subtt, sz = sz2,
                      x=subtt_x, y=y, color = color2, spacing=spacing,
                ali = "left" ,bac_color=bac_color)
        y += int(sz2*2.5)
        postcard.postBoxText(sub_text, font=font_txt,  sz = sz3,
                      x=txt_x, y=y, color = color3, spacing=spacing,
                             ali = "left", bac_color=None)
        y += (sz3 + spacing) * len(sub_text) + 50
    return postcard.get_res()

def generate_template( pre_img, input_image,  mt_name,
                    font_title, sz1, title_x, title_y, color1,
                   font_subtt, sz2, subtt_x, subtt_y, color2,
                   font_txt,   sz3, txt_x,  color3, bac_color):
    if pre_img is None:
        print("Not debugged well, cannot save")
        return None
    if type(pre_img) is np.ndarray:
        template_img = f"./templates/{mt_name}.png"
        template_img_preview = f"./templates/{mt_name}.jpg"
        print("Saving image", template_img)
        pil = Image.fromarray(input_image)
        pil_2 = Image.fromarray(pre_img)
        pil_2.save(template_img_preview)
        pil.save(template_img)
    print("Start saving template")
    # Save template preview effect
    template_name = f"./templates/{mt_name}.csv"
    name = ["template_img","font_title", "sz1", "title_x", "title_y", "color1",
        "font_subtt", "sz2", "subtt_x", "subtt_y", "color2",
        "font_txt", "sz3", "txt_x", "color3", "bac_color"]
    value = [[template_img, font_title, sz1, title_x, title_y, color1,
                   font_subtt, sz2, subtt_x, subtt_y, color2,
                   font_txt,   sz3, txt_x,  color3, bac_color]]
    record = pd.DataFrame(data=value, columns=name)
    record.to_csv(template_name, index=False)
    return [os.path.join(templates_path,i) for i in os.listdir(templates_path) if i.endswith("jpg")]

def load_template(mt_name):
    template_name = f"./templates/{mt_name}.csv"
    template_img = f"./templates/{mt_name}.png"
    if not os.path.exists(template_name):
        print("Error on dealing this template name :", mt_name)
        return None
    template_df = pd.read_csv(template_name)
    print(template_df)
    return ["font_title", 12, 1, 1, "color1",
         "font_subtt", 12, 123, 1, "color2",
         "font_txt", 123, 12, "color3"]
     res = [template_img]
     res.extend()
    res = list(template_df.values[0])
    return res
   
def change_textbox(choice):
     #Update the output control based on different inputs
     if choice == "short":
         return gr.update(lines=2, visible=True, value="Short story: ")
     elif choice == "long":
         return gr.update(lines=8, visible=True, value="Long story...")
     else:
         return gr.update(visible=False)
 with gr.Blocks() as demo:
     radio = gr.Radio(
         ["short", "long", "none"], label="Essay Length to Write?"
     )
     text = gr.Textbox(lines=2, interactive=True)
     radio.change(fn=change_textbox, inputs=radio, outputs=text)
 demo.launch()

    
key_index =  ["bm_sj","fee_sj","ks_sj","zkz_sj"]
def generate_mv(bac_img, title, a,b,c,d,e,f, sz1, sz2, sz3, spacing, color1, color2):
    global movies, imgs_cur
    bing_dir = "./bingpost"
    front_imgs =[os.path.join(bing_dir,i) for i in os.listdir("./bingpost") if i.endswith(".png")]
    front_img = random.choice(front_imgs)
    if bac_img is None:
        bac_img = "./kaobianBottem.jpeg"
    imge_dir = "imgpost"
    fps = 1
    image_dur = 3
    movie_dir = "movie_output"

    msg = []
    new_title = title.replace('\n', "").replace('”', "").replace('“', "").replace(' ', "")
    output_wav = f"audio_output/{new_title}.wav"
    tts_cmd = f'edge-tts  --voice zh-CN-XiaoxiaoNeural  --rate=+10% --text "{title}" --write-media {output_wav} 2>&1 >/dev/null'
    _m = os.popen(tts_cmd).read()
    msg.append(_m)
    # image
    audio_file = AudioFileClip(output_wav)
    movie_file = f"{movie_dir}/{new_title}.mp4"
    img_files = []
    mv_image_files = []
    
    for k,lines in enumerate([title,a,b,c,d]):
        k = key_index[k]
        if not lines:
            # This key information is missing, skip
            continue
        if len(lines) < 2:
            continue
        lines = lines.split("\n")
        filename = f"{k}_{new_title}.png"
        filename = os.path.join(imge_dir, filename)
        img_files.append(filename)
        # --- How long a image last display
        for i in range(image_dur):   
            mv_image_files.append(filename)
        img = generatePost(lines=lines,front_img = front_img, bac_img = bac_img, fn_name = filename)

    # clip_img = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(img_files, fps=fps) #durations=audio_file.duration ) #
    if len(img_files) < 1:
        print("Error, this url did not get a valid key info:{new_title}")
        return "","",""
    clip_img = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(mv_image_files, fps=fps, durations=audio_file.duration ) #
    clip_img = clip_img.set_audio(audio_file)
    clip_img.write_videofile(movie_file, fps=fps)#, audio_codec="aac")
    print(movie_file, ":done")
    movies = [os.path.join(mv_path,i) for i in os.listdir(mv_path) if i.endswith("mp4")]
    # imgs = [os.path.join(img_path,i) for i in os.listdir(mv_path) if i.endswith("png")]
    imgs_cur = img_files
    return movie_file, img_files

def exit_func():
    driver.close()
    time.sleep(3)
    exit(1)

 def refresh_template():
     global templates_name
     templates_name = [i.strip(templates_path).strip(".csv") for i in templates]
     return templates_name
    
# Login Douyin
def loginDouyin():
    url = 'https://creator.douyin.com/'
    hm.set_driver(driver)  # Give it a selnuim driver
    hm.go_to(url)
    driver.get_screenshot_as_file("1.png")
    print("-------------------Please scan the QR code to log in to the Douyin Creator Center-------------------")
    hm.click(hm.Text("Log In"))
    time.sleep(1)
    hm.click(hm.Text("Confirm"))
    time.sleep(1)
    qr_element = driver.find_element_by_class_name("qrcode-image")
    qr_element.click()
    qr_element.screenshot("qr.png")
    return "qr.png"

def run_save_cookie(account_name):
    cookie_fns.append(account_name)
    cookie_file_name = cookie_f.format(account_name)
    save_cookie(driver, cookie_file_name)
    gr.Dropdown.update(choices=account_fn, value=cookie_fns)
    return "succ"

input_image_, font_title_, sz1_, title_x_, title_y_, color1_, \
    font_subtt_, sz2_, subtt_x_, subtt_y_, color2_, \
    font_txt_,   sz3_, txt_x_,  color3_, bac_color_ = load_template("Dedicated")
# Build Blocks context =======================================================================
with gr.Blocks() as demo:
    with gr.Tabs():
        # --------------generate movie -------------      
        with gr.TabItem("Generate & Preview"):
            gr.Markdown(f"# {VIPtitle}")
            gr.Markdown(f"{description}")
            with gr.Row():       # Row arrangement        
                with gr.Column():    # Column arrangement
                    title = gr.Textbox("Chaoyang District 2023 Public Institution Announcement",label="Title",interactive=True)
                    a = gr.Textbox("Title 1. Content",label="a")
                    b = gr.Textbox(lines=2, value = "Registration Time. March 10, 2023 to March 17, 2023, 24:00.", label="b",interactive=True)
                    c = gr.Textbox(lines=2, value = "Subtitle 1. Written Examination will be held on April 8, 2023", label="c",interactive=True)
                    d = gr.Textbox(lines=2, value = " ", label="d",interactive=True)
                    e = gr.Textbox(lines=2, value = " ", label="e",interactive=True)
                    f = gr.Textbox(lines=2, value =  " ", label="f",interactive=True)
                    
                # movie_file = gr.Video(exam_video,label="movie")
                with gr.Column():
                    # -- Input background image as canvas --
                    input_image = gr.Image(input_image_, label = "Background Image Input",interactive=True)
                    title_x = gr.Slider(1, WIDTH, label = "Title Horizontal Movement", value=title_x_, step = 5)
                    title_y = gr.Slider(1, HEIGHT, label = "Title Vertical Movement", value=title_y_, step = 5)
                    font_title = gr.Dropdown(choices = font_list, label = "Title Font", 
                                    value = font_title_)
                    sz1 = gr.Slider(1, 100, label = "Title Size", value=sz1_, step = 5)
                    color1 = gr.Textbox(color1_, label = "Title Color")
                    bac_color = gr.Textbox(bac_color_, label = "Text Box Color (leave blank for no box)")

                with gr.Column():
                    # -- Subtitle
                    font_subtt = gr.Dropdown(choices = font_list, label = "Subtitle Font", value = font_subtt_)
                    sz2 = gr.Slider(1, 100, label = "Subtitle Size", value=sz2_, step = 5)
                    subtt_x = gr.Slider(1, WIDTH, label = "Subtitle Horizontal Movement", value=subtt_x_, step = 5)
                    subtt_y = gr.Slider(1, HEIGHT, label = "Subtitle Vertical Movement", value=subtt_y_, step = 5)
                    color2 = gr.Textbox(color2_, label = "Subtitle Color")
                    font_txt = gr.Dropdown(choices = font_list, label = "Text Font", value = font_txt_)
                    sz3 = gr.Slider(1, 100, label = "Text Size", value=sz3_, step = 5)
                    txt_x = gr.Slider(1, WIDTH, label = "Content Position X", value=txt_x_, step = 5)
                    color3 = gr.Textbox(color3_, label = "Text Color")

            with gr.Row():
                with gr.Column():       # ----Button Controls------
                    pre_img_bt = gr.Button("Preview")
                    record_template = gr.Button("Export Template")
                    mt_name = gr.Textbox("Template_v1",label="Template Name (required for export)")
                    # font_txt = gr.Dropdown(choices = font_list, label = "文本字体", value = "fonts/simsun.ttc")
                    mt_selected = gr.Dropdown(choices = templates_name, label = "Select Template to Load")
                    load_mt = gr.Button("Load Template Parameters")
                 submit = gr.Button("生成")
                 account_fn = gr.Dropdown(choices=cookie_fns, label = "账号选择", value = "抖音广东人事考试")
                 with gr.Column():
                pre_img2 = gr.Image(label="Generated Result Preview", interactive=False)
                with gr.Row():
                    gallery = gr.Gallery(
                        value = preview_templates,
                        label="Preview", show_label=True, elem_id="gallery"
                        ).style(columns=[3], rows=[2], object_fit="contain", height="auto")
            
                     mv_files = gr.Files(movies, label="movies")
                     img_files = gr.Files(imgs_cur, label="movie_imgs")

        with gr.TabItem("Generate & Publish"):
            gr.Markdown(f"{description}")
            with gr.Row():       # Row arrangement        
                with gr.Column():    # Column arrangement
                    title1 = gr.Textbox("Chaoyang District 2023 Recruitment of Public Institution Personnel Announcement",label="Title")
                    a1 = gr.Textbox("xxxx",label="a")
                    b1 = gr.Textbox(lines=2, value = "Registration Time. March 10, 2023 to March 17, 2023, 24:00.", label="b")
                    c1 = gr.Textbox(lines=2, value = "Payment Time. May 27, 2023", label="c")
                    d1 = gr.Textbox(lines=2, value = "Subtitle 1. Written Examination will be held on April 8, 2023", label="d")
                    e1 = gr.Textbox(lines=2, value = "Subtitle 2. Print your admission ticket from the Guangyuan Personnel Examination Website.", label="e")
                    f1 = gr.Textbox(lines=2, value =  "Subtitle 3. See Admission Ticket.", label="f")
                    
                with gr.Column():
                    # Upload the finished image to generate
                    input_image_2 = gr.Image(background_img, label = "Background Image Input",interactive=True)
                    
            with gr.Row():
                with gr.Column():       # ----Button Controls------
                    post_img_bt = gr.Button("Test Publish")
                    refresh_template_bt = gr.Button("Refresh Templates")
                    # mt_name = gr.Textbox("模板_v1",label="导出模板必填名字")
                    mt_name_selected = gr.Dropdown(choices = templates_name, label = "Select Template for Generation")
                # pre_img2 = gr.Image(label="生成结果预览", interactive=False)

        with gr.TabItem("Todo Embedded Browser PyQt Html"):
            mp = gr.HTML(html, elem_id="coords", visible=True)
            pass
            
    pre_img_bt.click(fn=generate_image, inputs=[input_image, title,a,b,c,d,e,f, 
                   font_title, sz1, title_x, title_y, color1,
                   font_subtt, sz2, subtt_x, subtt_y, color2,
                   font_txt,   sz3, txt_x,  color3, bac_color],
                  outputs=[pre_img2])
    record_template.click(fn=generate_template, inputs=[pre_img2, input_image, mt_name,
                   font_title, sz1, title_x, title_y, color1,
                   font_subtt, sz2, subtt_x, subtt_y, color2,
                   font_txt,   sz3, txt_x,  color3, bac_color],
                  outputs=[gallery])
    load_mt.click(fn=load_template, 
                  inputs = [mt_selected],
                  outputs=[input_image, font_title, sz1, title_x, title_y, color1,
                   font_subtt, sz2, subtt_x, subtt_y, color2,
                   font_txt,   sz3, txt_x,  color3, bac_color])
    
     refresh_template_bt.click(fn=refresh_template, inputs=None, outputs=[templates_name])
     template_params = []
     post_img_bt.click(inputs = [title, a,b,c,d,e,f])  # Used to append template parameters, concise version
     submit.click(fn=generate_mv, inputs=[title, a,b,c,d], 
                  outputs=[img_files])
                  outputs=[movie_file, img_files])
     exit_.click(fn=exit_func)
     login_.click(fn=loginDouyin, outputs=[login_qr])
     login_save.click(fn=run_save_cookie, inputs = [account_name_new])
     post_.click(fn=mySendDouyin, inputs = [account_fn, movie_file])
     Bind clear click function
     clear.click(fn=clear_input, inputs=[], outputs=[context, question, answer, score])


if __name__ == "__main__":
    demo.queue().launch()
    print("Run from current")
