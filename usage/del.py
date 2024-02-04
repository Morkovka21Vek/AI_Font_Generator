from PIL import Image
import os

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
strq='Выберите пожалуйста какой шрифт вы хотите использовать(напишите номер):\n'
for i in range(len(files)):
    strq += '[' + str(i) + ']' + files[i] + '\n'
strq += '>>>'
num = int(input(strq))
try:
    directory = directory + '\\' + files[num]
    print(directory)
    files = os.listdir(directory)
    delete(files, directory)
except IndexError:
    print('Вы ввели несущиствующий номер!(ENTER чтобы выйти)')
    input()
except Exception:
    print('Неизвестная ошибка! Обратитеть в автору нейросети.(ENTER чтобы выйти)')
    input()
