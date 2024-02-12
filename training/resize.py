from PIL import Image
import os
import json

with open(os.path.abspath(os.getcwd())+'\\settings.json', encoding='utf-8') as f:
    language = json.load(f)["Language"]

def resize_images(input_path, output_path, new_size=(40, 40)):
    # Open the image
    img = Image.open(input_path)

    # Resize the image
    resized_img = img.resize(new_size)

    # Save the resized image
    resized_img.save(output_path)

directory = os.path.realpath('out_png')
files = os.listdir(directory)
x = int(input(language["SizeX"]))
y = int(input(language["SizeY"]))
for f in files:
    filename = directory + '\\' + f
    im = Image.open(filename)
    resize_images(filename, filename, (x,y))
    
    # F[name].export(filename, 600)     # set height to 600 pixels

print(language["Programm_End"])
input()
