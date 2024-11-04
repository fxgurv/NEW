# coding: utf-8
# 1、根据背景底板 设定图像大小
# 2、
import pandas as pd
import os
import random
import IPython.display as ipd
import numpy as np

import moviepy.video.io.ImageSequenceClip
from moviepy.editor import AudioFileClip,TextClip,CompositeVideoClip


from txtImgPost import  myPost, reshape_texts, generatePost
import inspect, math
from PIL import Image, ImageDraw, ImageFont

# for img_post
result_post_file = "post_v1.png"
import random
# front_img = "./bingpost/2023-05-13.png"
bing_dir = "./bingpost"
front_imgs =[os.path.join(bing_dir,i) for i in os.listdir("./bingpost") if i.endswith(".png")]
front_img = random.choice(front_imgs)
print(front_img)

bac_img = "./kaobianBottem.jpeg"
imge_dir = "imgpost"
key_index =  {"bm_sj":8+4,"fee_sj":9+ 4,"ks_sj":14,"zkz_sj":15}

# for movie Param
fps = 1
image_dur = 3
movie_dir = "movie_output"

target_dir = "scrap_data/"

res_list = [os.path.join(target_dir,i) for i in os.listdir(target_dir) if i.endswith(".csv")]
# res_list

fn = "scrap_data/2023-05-14_01:21.csv"

df = pd.read_csv(fn)
for i in df.columns:
    if np.all(pd.notnull(df[i])) == False:
        df[i].fillna("", inplace=True)
df.head()

# 生成音频
msg = []
# 生成音频
# for it in task_docs:
for it in df.itertuples():    
    # title = it["title"]
    title = it[2]
    new_title = title.replace('\n', "").replace('”', "").replace('“', "").replace(' ', "")
    output_wav = f"audio_output/{new_title}.wav"
    tts_cmd = f'edge-tts  --voice zh-CN-XiaoxiaoNeural  --rate=+10% --text "{title}" --write-media {output_wav} 2>&1 >/dev/null'
    print(title)
    _m = os.popen(tts_cmd).read()
    msg.append(_m)


# record: url title audio_file imgs[ks_sj, bm_sj]__file, movie_file_name
# for it in task_docs:
records_all = []
for it in df.itertuples():    # all doc_item url content
    # title = it["title"]
    title = it[2]
    new_title = title.replace('\n', "").replace('”', "").replace('“', "").replace(' ', "")
    output_wav = f"audio_output/{new_title}.wav"
    audio_file = AudioFileClip(output_wav)
    movie_file = f"{movie_dir}/{new_title}.mp4"
    imgs = []
    img_files = []
    image_files = []
    title = it[2]
    new_title = title.replace('\n', "").replace('”', "").replace('“', "").replace(' ', "")
    for k,v in key_index.items():
        lines = it[v]
        url_ = it[1]
        if len(lines) < 1:
            continue
        lines = lines.split("\n")
        filename = f"{k}_{new_title}.png"
        filename = os.path.join(imge_dir, filename)
        img_files.append(filename)
        # --- how long a image last display
        for i in range(image_dur):   
            image_files.append(filename)
        img = generatePost(lines=lines,front_img = front_img, bac_img = bac_img, fn_name = filename)
        imgs.append(img)
    # clip_img = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(img_files, fps=fps) #durations=audio_file.duration ) #
    if len(img_files) < 1:
        print("error, this url not get a valid key info:{new_title},url:{url_}")
        continue
    clip_img = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps, durations=audio_file.duration ) #
    clip_img = clip_img.set_audio(audio_file)
    clip_img.write_videofile(movie_file, fps=fps)#, audio_codec="aac")
    print(movie_file, ":done")
    rec_ = [new_title, output_wav, movie_file]
    rec_.append(img_files)
    records_all.append(rec_)
    
