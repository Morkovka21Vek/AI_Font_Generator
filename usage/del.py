from PIL import Image
import os
import json

with open(os.path.abspath(os.getcwd())+'\\language.json', encoding='utf-8') as f:
    language = json.load(f)

def delete(files, directory):
    for f in files:
        filename = directory + '\\' + f
        im = Image.open(filename)
        flag = False
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                #print(im.getpixel((x, y)), f)
                if im.getpixel((x, y)) != 0:
                    flag = True
        if flag == False:
            os.remove(filename)
            print('del: ', filename)

            
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
    delete(files, directory)
    print(language["Programm_End"])
    input()
except IndexError:
    print(language["ErrorNumber"])
    input()
except Exception as e:
    print(language["Exception"], e)
    input()
