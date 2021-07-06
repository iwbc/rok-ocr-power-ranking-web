# coding: UTF-8

import sys
import os
import glob
import re
import cv2
import pytesseract
import numpy as np
from PIL import Image

def ocr_individuals():
    global individual_powers
    img_paths = sorted(glob.glob(images_dir + '/*'))

    for img_path in img_paths:
        f_name = os.path.split(img_path)[1]
        tmp_img_path = tmp_dir + '/' + f_name

        print(os.path.basename(img_path))

        img = correct_image(img_path, tmp_img_path)
        ocr_data = ocr(img)
        data = normalize_data(ocr_data, img_path)
        individual_powers = np.append(individual_powers, data)


def ocr(img):
    res = pytesseract.image_to_string(
        img, lang="eng", config='--psm 6 -c tessedit_char_whitelist="0123456789"')
    print(res)
    return res


def correct_image(img_path, tmp_img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (2560, 1440), interpolation=cv2.INTER_LINEAR)
    ret, img = cv2.threshold(img, 115, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_not(img)
    cv2.imwrite(tmp_img_path, img)

    img = Image.open(tmp_img_path)
    img = img.crop((1813, 379, 2135, 1380))
    img.save(tmp_img_path)

    return img


def normalize_data(data, img_path):
    normalized_data = []
    prev_power = None
    has_warning = False

    for d in data.splitlines():
        power = d.strip()
        if re.fullmatch('[0-9]+', power):
            power = int(power)
            if prev_power is not None and prev_power < power:
              has_warning = True
            normalized_data.append(power)
            prev_power = power

    if has_warning is True:
      global warning
      warning.append(os.path.basename(img_path))

    if len(normalized_data) != 6:
        print('Error: OCRに失敗しました → ' + os.path.basename(img_path))
        sys.exit(1)

    return normalized_data


#########################################################################################################


images_dir = sys.argv[1]
tmp_dir = sys.argv[2]
individual_powers = np.array([], dtype=int)
warning = []

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

ocr_individuals()

ip = str(np.sum(individual_powers))
ip_ave = str(round(np.mean(individual_powers)))
o150m = str(np.count_nonzero(individual_powers >= 150000000))
o140m = str(np.count_nonzero(individual_powers >= 140000000))
o130m = str(np.count_nonzero(individual_powers >= 130000000))
o120m = str(np.count_nonzero(individual_powers >= 120000000))
o110m = str(np.count_nonzero(individual_powers >= 110000000))
o100m = str(np.count_nonzero(individual_powers >= 100000000))
o90m = str(np.count_nonzero(individual_powers >= 90000000))
o80m = str(np.count_nonzero(individual_powers >= 80000000))
o70m = str(np.count_nonzero(individual_powers >= 70000000))
o60m = str(np.count_nonzero(individual_powers >= 60000000))
o50m = str(np.count_nonzero(individual_powers >= 50000000))
o40m = str(np.count_nonzero(individual_powers >= 40000000))
o30m = str(np.count_nonzero(individual_powers >= 30000000))
o20m = str(np.count_nonzero(individual_powers >= 20000000))

print("合計\t平均\t150M\t140M\t130M\t120M\t110M\t100M\t90M\t80M\t70M\t60M\t50M\t40M\t30M\t20M")
print(ip + "\t" + ip_ave + "\t" + o150m + "\t" + o140m + "\t" + o130m + "\t" + o120m + "\t" + o110m +
            "\t" + o100m + "\t" + o90m + "\t" + o80m + "\t" + o70m + "\t" + o60m + "\t" + o50m + "\t" + o40m + "\t" + o30m + "\t" + o20m)

for w in warning:
  print("\nWarning: 正しく数値が読み取れなかった可能性があります → " + w)

print("\n----------Done!----------")
