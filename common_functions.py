# -*- coding: utf-8 -*-
#版本 1.50
#作者：晓天
#时间：29/7/2023

import os
import shutil
from PIL import Image
from tqdm import tqdm
from pprint import pprint
from time import strftime, localtime
from typing import List, Dict, Union, Tuple
from moviepy.editor import *
from moviepy.config import change_settings
from pillow_heif import register_heif_opener


def pro_slash(strs: str) -> str:
    """
    消除字符串中多余的转义符。
    """
    re_strs = repr(strs)
    while '\\\\' in re_strs:
        re_strs = re_strs.replace('\\\\', '\\')
    if re_strs[-2] == '\\':
        print(re_strs[1:-2])
        re_strs = re_strs[1:-2]

    try:
        pro_strs = eval(re_strs)
        return pro_strs
    except Exception as e:
        print(e)
        return strs

def creat_folder(path: str) -> str:
    """
    判断系统是否存在该路径，没有则创建。
    """
    while True:
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            break
        except FileNotFoundError:
            path = path[:-1]
            continue
    return path

def str_to_dict(strs: str) -> Dict[str, str]:
    """
    将字符串转化为字典。
    """
    header = strs.split('\n')
    headers = {}
    
    while '' in header:
        header.remove('')

    for h in header:
        if h[0] == ':':
            h = h[1:]
        sp = h.partition(':')
        headers[sp[0]] = sp[2].strip()

    return headers

def list_removes(lists: list, _remove) -> list:
    while _remove in lists:
        lists.remove(_remove)
    return lists

def str_removes(strs: str, _remove: str) -> str:
    """
    从字符串中移除指定的子串。
    
    Args:
        strs (str): 原始字符串。
        _remove (str): 需要从原始字符串中移除的子串。
    
    Returns:
        str: 移除指定子串后的新字符串。
    """
    return strs.replace(_remove, '')

def list_replace(lists: List[str], replace_list: List[Tuple[str, str]]) -> List[str]:
    """
    替换列表中的字符串。
    """
    new_list = []
    for l in lists:
        for r in replace_list:
            l = l.replace(r[0], r[1])
        new_list.append(l)
    return new_list

def str_replaces(strs: str, replace_list: list) -> str:
    for r in replace_list:
        strs = strs.replace(r[0], r[1])
    return strs

def iprint(obj: Union[List, Dict], start='', end=''):
    """
    根据对象的大小选择打印方式。
    如果对象的长度小于16，那么就打印整个对象，否则只打印前10个和后5个元素。

    Args:
        obj (Union[List, Dict]): 需要打印的对象，可以是列表或字典。
    """
    print(start, end='')
    length = len(obj)
    if length < 16:
        pprint(obj)
    else:
        pprint(obj[:10])
        print(f'(此处省略{length-15}项)')
        pprint(obj[-5:])
    print(end, end='')

def count_occurrences(lst: List[Tuple[Tuple[str, int], str]], value: str) -> int:
    """
    在列表中查找指定元素的出现次数。
    
    Args:
        lst (List[Tuple[Tuple[str, int], str]]): 原始列表，列表的元素是元组，元组的第一个元素是字符串。
        value (str): 需要查找的元素。

    Returns:
        int: 指定元素在列表中的出现次数。
    """
    return sum(1 for item in lst if item[0][0] == value)

def get_key_dict(lst: List[Tuple[str, int]]) -> Dict[str, Tuple[int]]:
    """
    从列表中获取键值对，创建并返回一个字典。
    
    Args:
        lst (List[Tuple[str, int]]): 原始列表，列表的元素是元组。

    Returns:
        Dict[str, Tuple[int]]: 从列表中获取的键值对组成的字典。
    """
    dict_result = {}
    for item in lst:
        key, value = item[0][0], item[0][1]
        dict_result.setdefault(key, []).append(value)
    return {key: tuple(values) for key, values in dict_result.items()}

def find_tuple(lst: List[Tuple[Tuple[str, int], str]], target: str) -> Tuple[str, int]:
    """
    在列表中查找指定的元组。
    
    Args:
        lst (List[Tuple[Tuple[str, int], str]]): 原始列表，列表的元素是元组。
        target (str): 需要查找的元素。

    Returns:
        Tuple[str, int]: 在列表中找到的元组，如果没有找到，则返回None。
    """
    return next((item for item in lst if item[0] == target), None)

def strings_spit(*strs, split_str = '\n'):
    li = []
    for num,st in enumerate(strs):
        li.append(st.split(split_str))
        li[-1] = list_removes(li[num], '')
    
    return li

def dictkey_mix(dict_a: dict, dict_b: dict):
    key_a = list(dict_a.keys())
    key_b = list(dict_b.keys())

    key_max = key_a[:]
    key_min = []
    dif_key_a = []
    dif_key_b = []
    
    for each in key_b:
        if each not in key_a:
            key_max.append(each)
            dif_key_b.append(each)
        else:
            key_min.append(each)
    for each in key_a:
        if each not in key_b:
            key_max.append(each)
            dif_key_a.append(each)
    
    return key_max,key_min,dif_key_a,dif_key_b

def deal_cookie(*cookies):
    cookie_dicts = []
    for cookie in cookies:
        #cookie += '; '

        cookie_list = cookie.split('; ')
        cookie_dict = {}
        for c_l in cookie_list:
            #print(c_l)
            key,_,value = c_l.partition('=')
            cookie_dict[key] = value
        cookie_dicts.append(cookie_dict)

    return cookie_dicts

def get_now_time():
    return strftime("%Y-%m-%d", localtime())
    
def join_and_label_videos(video_path1, video_path2, output_path):
    change_settings({"IMAGEMAGICK_BINARY": r"G:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

    # 加载视频，设置持续时间为10秒
    clip1 = VideoFileClip(video_path1).subclip(0, 10)
    clip2 = VideoFileClip(video_path2).subclip(0, 10)

    # 在视频左上角添加文本标签
    video_name1 = os.path.basename(video_path1)
    video_name2 = os.path.basename(video_path2)

    txt_clip1 = TextClip(video_name1, fontsize=24, color='white')
    txt_clip1 = txt_clip1.set_position(('left', 'top')).set_duration(10)
    
    txt_clip2 = TextClip(video_name2, fontsize=24, color='white')
    txt_clip2 = txt_clip2.set_position(('left', 'top')).set_duration(10)

    # 将文本标签与视频组合
    video_with_label1 = CompositeVideoClip([clip1, txt_clip1])
    video_with_label2 = CompositeVideoClip([clip2, txt_clip2])

    # 将两个视频左右拼接
    final_video = clips_array([[video_with_label1, video_with_label2]])

    # 保存结果
    final_video.write_videofile(output_path, fps=24)

def compress_fold(folder_path):
    register_heif_opener()
    Image.LOAD_TRUNCATED_IMAGES = True
    Image.MAX_IMAGE_PIXELS = None
    
    # 创建新文件夹
    new_folder_path = os.path.join(os.path.dirname(folder_path), os.path.basename(folder_path) + "_re")
    os.makedirs(new_folder_path, exist_ok=True)
    error_list = []
    img_snuffix = ["jpg", "png", "jpeg", 'heic', 'webp', "JPG", "PNG", "JPEG", "HEIC", "WEBP"] # 'heic', "HEIC"
    video_snuffix = ["mp4", "avi", "mov", "mkv", 'divx', "mpg", "flv", "rm", "rmvb", "mpeg", "wmv", "3gp", "vob", "ogm", "ogv", "asf",
                     "MP4", "AVI", "MOV", "MKV", 'DIVX', "MPG", "FLV", "RM", "WMV", "3GP", "TS"]

    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        for filename in tqdm(files):
            # 如果是图片
            if filename.split('.')[-1] in img_snuffix:
                old_img_path = os.path.join(root, filename)
                new_img_path = os.path.join(new_folder_path, 
                                            os.path.relpath(old_img_path, folder_path))
                
                # 如果已经存在，则跳过
                if os.path.exists(new_img_path):
                    continue
                os.makedirs(os.path.dirname(new_img_path), exist_ok=True)
                
                try:
                    # 打开图片并压缩
                    img = Image.open(old_img_path)
                    img.save(new_img_path, optimize=True, quality=50)
                except OSError as e:
                    error_list.append((old_img_path,e))
                    shutil.copy(old_img_path, new_img_path)
                    continue
            # 如果是视频
            elif filename.split('.')[-1] in video_snuffix:
                old_video_path = os.path.join(root, filename)
                new_video_path = os.path.join(new_folder_path, 
                                              '_'.join(os.path.relpath(old_video_path, folder_path).split('.')[:-1])).replace('_compressed', '')
                new_video_path += '_compressed.mp4'
                os.makedirs(os.path.dirname(new_video_path), exist_ok=True)
                
                # 如果已经存在，则跳过
                if os.path.exists(new_video_path):
#                     print(new_video_path)
                    continue
                # 如果已经是压缩后的视频，则复制过去
                elif '_compressed.mp4' in filename:
                    shutil.copy(old_video_path, new_video_path)
                    continue
                    
                # 使用ffmpeg压缩视频
#                 print(f'ffmpeg -i "{old_video_path}" -vcodec libx264 -crf 24 "{new_video_path}"')
                os.system(f'ffmpeg -i "{old_video_path}" -vcodec libx264 -crf 24 "{new_video_path}"')
            # 如果是其他文件，则直接复制
            else:
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(new_folder_path, os.path.relpath(old_file_path, folder_path))
                
                # 如果已经存在，则跳过
                if os.path.exists(new_file_path):
                    continue
                    
                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                shutil.copy(old_file_path, new_file_path)

    return error_list
if __name__ == '__main__':
    a = '(W//R\S/H\\U)'
    b = "https:\/\/m10.music.126.net\/20211221203525\/cb633fbb6fd0423417ef492e2225ba45\/ymusic\/7dbe\/b17e\/1937\/9982bb924f5c3adc6f85679fcf221418.mp3"
    #t = pro_slash(a)

    join_and_label_videos(
    r'F:\下载\魔法擦除_20230731_1(1)\temp\chf3_prob3.mp4', 
    r'F:\下载\魔法擦除_20230731_1(1)\temp\chf3_prob3_stab_thm2.mp4',
    r'F:\下载\魔法擦除_20230731_1(1)\temp\mix.mp4'
                        )
    
    pass
    


