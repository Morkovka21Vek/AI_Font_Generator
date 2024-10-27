from fontTools.ttLib import TTFont
from freetype import Face, FT_Curve_Tag, FT_Curve_Tag_On, FT_Vector

import os
from glob import glob
import string
from tqdm import tqdm
from svg.path import parse_path
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
import numpy as np
import math

import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.TtfSvgConverter import TtfSvgConverter

cyrillic_lower_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
desiredLetters = string.ascii_uppercase + cyrillic_lower_letters.upper()
# desiredLetters = list(string.ascii_uppercase) + list(cyrillic_lower_letters.upper())
desiredLetters = [ord(i) for i in desiredLetters]


def extract_path(name, freq, scale=1, x_offset=0, y_offset=0):
    doc = ET.fromstring(name)
    # path_strings = [path.attrib['d'] for path in doc.find('path')]#[path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    path_strings = [path.attrib['d'] for path in doc.findall('.//{http://www.w3.org/2000/svg}path')]

    allItemsCount = sum(len(parse_path(path_string)) for path_string in path_strings)#0
    # for path_string in path_strings:
    #     items = parse_path(path_string)
    #     allItemsCount += len(items)
    AddPointCount = freq - allItemsCount*int(freq/allItemsCount)
    step = allItemsCount/freq
    path = []
    path2 = []
    for path_string in path_strings:
        items = parse_path(path_string)
        for item in items:
            AddPointCount -= 1
            for i in range(int(freq/allItemsCount) + (1 if AddPointCount >= 0 else 0)):
                if i == 0:
                    pos2 = item.point(step*i)
                    path2.append([(pos2.real+x_offset)*scale, (pos2.imag+y_offset)*scale])
                pos = item.point(step*i)
                path.append([(pos.real+x_offset)*scale, (pos.imag+y_offset)*scale])
                if False:
                    pos2 = item.point(step*i+step/2)
                    path.append([(pos2.real+x_offset)*scale, (pos2.imag+y_offset)*scale])
    return path, path2

def font2arr(pathToFont: str, fontName: str):
    paths = {}
    font_obg = TTFont(pathToFont)
    m_dict = font_obg.getBestCmap()
    if not m_dict:
        return
    converter = TtfSvgConverter(ttfPath=pathToFont)
    for key, text in m_dict.items():
        if key in desiredLetters:
            xml = converter.generate(text, os.path.join(os.path.dirname(os.path.abspath(__file__)), "trainingDataset", f"{fontName}__{str(key)}.svg"), mode=1)
            if xml == None:
                continue
            path, path2 = extract_path(xml, 100)
            path = np.array(path)
            path2 = np.array(path2)
            # path = (path-np.min(path))/(np.max(path)-np.min(path))
            # path2 = (path2-np.min(path))/(np.max(path)-np.min(path))
            paths[str(key)] = path
            # plt.plot(path[:, 0], path[:, 1], "ro")
            # plt.show()
            plt.plot(path[:, 0], path[:, 1]*-1+1)
            plt.plot(path2[:, 0], path2[:, 1]*-1+1, "bo")
            for i, pos in enumerate(path2):
                plt.text(pos[0], pos[1]*-1+1, str(i), color="r")#, fontsize="x-small"
            plt.show()
    if paths != {}:
        pass
        # np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "trainingDatasetArray", f"{fontName}.npz"), **paths)
        
if __name__ == "__main__":
    #folderFontPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trainingFonts")
    folderFontPath = "C:\\Users\\User\\Documents\\GitHub\\AI_Font_Generator\\training\\trainingFontsTest"#"C:\\Users\\User\\Documents\\AI_Font_Generator\\trainingFonts"
    # listFonts = os.listdir(folderFontPath)
    # fullListFonts = [os.path.join(folderFontPath, i) for i in listFonts]
    # fullListFonts = [y for x in os.walk(folderFontPath) for extension in ['*.ttf', '*.otf', '*.TTF', '*.OTF', '*.pfm', '*.pfb', '*.PFM', '*.PFG'] for y in glob(os.path.join(x[0], extension))]
    fullListFonts = [y for x in os.walk(folderFontPath) for extension in ['*.ttf', '*.otf', '*.TTF', '*.OTF'] for y in glob(os.path.join(x[0], extension))]
    print(len(fullListFonts))
    fullListFonts = fullListFonts[:1000]
    print(len(fullListFonts))
    for fontPath in tqdm(fullListFonts):
        font2arr(fontPath, os.path.basename(fontPath).split('.')[0])
