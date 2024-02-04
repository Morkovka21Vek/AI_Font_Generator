from PIL import Image
import os

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
strq='Выберите пожалуйста какой шрифт вы хотите использовать(напишите номер):\n'
for i in range(len(files)):
    strq += '[' + str(i) + ']' + files[i] + '\n'
strq += '>>>'
num = int(input(strq))
try:
    directory = directory + '\\' + files[num]
    print(directory)
    files = os.listdir(directory)
    crop(files, directory)
except IndexError:
    print('Вы ввели несущиствующий номер!(ENTER чтобы выйти)')
    input()
except Exception:
    print('Неизвестная ошибка! Обратитеть в автору нейросети.(ENTER чтобы выйти)')
    input()
