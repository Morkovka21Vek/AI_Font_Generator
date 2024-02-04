from PIL import Image
import os

def resize_images(input_path, output_path, new_size=(40, 40)):
    # Open the image
    img = Image.open(input_path)

    # Resize the image
    resized_img = img.resize(new_size)

    # Save the resized image
    resized_img.save(output_path)

def resize(files, directory):
    x = int(input('Введите пожалуйста размер по оси x: >>>'))
    y = int(input('Введите пожалуйста размер по оси y: >>>'))
    for f in files:
        filename = directory + '\\' + f
        im = Image.open(filename)
        resize_images(filename, filename, (x,y))


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
    resize(files, directory)
except IndexError:
    print('Вы ввели несущиствующий номер!(ENTER чтобы выйти)')
    input()
except Exception:
    print('Неизвестная ошибка! Обратитеть в автору нейросети.(ENTER чтобы выйти)')
    input()
