from PIL import Image
import os
import json
import traceback


def resize_images(input_path, output_path, new_size=(40, 40)):
    # Open the image
    img = Image.open(input_path)

    # Resize the image
    resized_img = img.resize(new_size)

    # Save the resized image
    resized_img.save(output_path)

def resize(files, directory):
    x = int(input(language["SizeX"]))
    y = int(input(language["SizeY"]))
    for f in files:
        filename = directory + '\\' + f
        im = Image.open(filename)
        resize_images(filename, filename, (x,y))

try:
    with open(os.path.abspath(os.getcwd())+'\\language.json', encoding='utf-8') as f:
        language = json.load(f)
    directory = os.path.realpath('out_png')
    files = os.listdir(directory)
    strq=language["SelectFont"]
    for i in range(len(files)):
        strq += '[' + str(i) + ']' + files[i] + '\n'
    strq += '>>>'
    num = int(input(strq))
    directory = directory + '\\' + files[num]
    print(directory)
    files = os.listdir(directory)
    resize(files, directory)
    print(language["Programm_End"])
    input()
except IndexError:
    print(language["ErrorNumber"])
    input()
except Exception:
    input(language["Exception"], traceback.print_exc())
