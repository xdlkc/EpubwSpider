import pytesseract as pt
import requests
from PIL import Image


def transform_eng(fp, lang=None):
    """
    图片转中文
    @param fp:定位符，支持http，https，本地目录
    @param lang：语言，默认英文，ch代表中文
    """
    if str(fp).startswith("http://") or str(fp).startswith("https://"):
        img = Image.open(requests.get(fp, stream=True).raw)
    else:
        img = Image.open(fp)
    if lang is 'ch':
        return pt.image_to_string(img, lang='chi_sim')
    else:
        return pt.image_to_string(img)

