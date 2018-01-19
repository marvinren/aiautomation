# -*- coding: UTF-8 -*-

from PIL import Image
import pytesseract
from selenium import webdriver


# 剪切图片
def cut_image(img_file, x=0, y=0, w=0, h=0):
    img = Image.open(img_file)

    region = img.crop((x, y, x + w, y + h))

    file_1 = '../img/region_1.png'
    region.save(file_1)

    return file_1


# 清除噪点
def clear_noise(img_file):
    # 读入图片
    img = Image.open(img_file)
    img = img.convert("RGBA")

    pixdata = img.load()

    # 二值化
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)

    file_2 = '/Users/reinhart/PycharmProjects/img/region_2.png'
    img.save(file_2)

    return file_2


# 识别图片
def ocr_text(img_file):
    try:
        img = Image.open(img_file)
        # img.load()
        text = pytesseract.image_to_string(img, 'eng')
    except Exception, e:
        print e
        text = ''

    return text


if __name__ == "__main__":
    wd = webdriver.Chrome()

    try:
        url = 'http://www.360doc.com/content/12/1006/21/9369336_239836993.shtml'
        wd.get(url)
        # wd.set_window_size(2464, 1554)
        img_path = '../img/region.png'
        wd.get_screenshot_as_file(img_path)

        file_1 = cut_image(img_path, 50, 908, 120, 40)

        file_2 = clear_noise(file_1)

        txt = ocr_text(file_2)

        print 'text=' + txt
    except Exception, ex:
        print ex

    wd.quit()
