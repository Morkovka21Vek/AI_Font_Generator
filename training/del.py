from PIL import Image
import os
import json

with open(os.path.abspath(os.getcwd())+'\\settings.json', encoding='utf-8') as f:
    language = json.load(f)["Language"]

directory = os.path.realpath('out_png')
files = os.listdir(directory)
for f in files:
    filename = directory + '\\' + f
    im = Image.open(filename)
    flag = False
    #print(im.size[0])
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            #print(im.getpixel((x, y)), f)
            if im.getpixel((x, y)) != 0:
                flag = True
    if flag == False:
        os.remove(filename)
        print('del: ', filename)
    # F[name].export(filename, 600)     # set height to 600 pixels
print(language["Programm_End"])
input()
