from PIL import Image
import os
import json

with open(os.path.abspath(os.getcwd())+'\\language.json', encoding='utf-8') as f:
    language = json.load(f)

def xRF(img):
    xR = 0
    for x in range(img.size[0]):
        flag = False
        for y in range(img.size[1]):
            #print(im.getpixel((x, y)), f)
            if img.getpixel((x, y)) != 0:
                flag = True
        if flag == False and xR <= x:
            xR = x
        else:
            return xR

def yUF(img):
    yU = 0
    for y in range(img.size[1]):
        flag = False
        for x in range(img.size[0]):
            #print(im.getpixel((x, y)), f)
            if img.getpixel((x, y)) != 0:
                flag = True
        if flag == False and yU <= y:
            yU = y
        else:
            return yU

def xLF(img):
    xL = img.size[0]
    for x in range(img.size[0]-1, -1, -1):
        flag = False
        for y in range(img.size[1]):
            #print(im.getpixel((x, y)), f)
            if img.getpixel((x, y)) != 0:
                flag = True
        if flag == False and xL >= x:
            xL = x
        else:
            return xL
        
def yDF(img):
    yD = img.size[1]
    for y in range(img.size[1]-1, -1, -1):
        flag = False
        for x in range(img.size[0]):
            #print(im.getpixel((x, y)), f)
            if img.getpixel((x, y)) != 0:
                flag = True
        if flag == False and yD >= y:
            yD = y
        else:
            return yD
def crop(files, directory):
    for f in files:
        filename = directory + '\\' + f
        im = Image.open(filename)
        im = im.crop((xRF(im), yUF(im), xLF(im), yDF(im)))
        #print((xRF(im), yUF(im), xLF(im), yDF(im)))
        im.save(filename)


directory = os.path.realpath('out_png')
files = os.listdir(directory)
strq=language["SelectFont"]
for i in range(len(files)):
    strq += '[' + str(i) + ']' + files[i] + '\n'
strq += '>>>'
num = int(input(strq))
try:
    directory = directory + '\\' + files[num]
    print(directory)
    files = os.listdir(directory)
    crop(files, directory)
    print(language["Programm_End"])
    input()
except IndexError:
    print(language["ErrorNumber"])
    input()
except Exception as e:
    print(language["Exception"], e)
    input()
