from PIL import Image
import os

def resize_images(input_path, output_path, new_size=(40, 40)):
    # Open the image
    img = Image.open(input_path)

    # Resize the image
    resized_img = img.resize(new_size)

    # Save the resized image
    resized_img.save(output_path)

directory = os.path.realpath('out_png')
files = os.listdir(directory)
x = int(input('Введите пожалуйста размер по оси x: >>>'))
y = int(input('Введите пожалуйста размер по оси y: >>>'))
for f in files:
    filename = directory + '\\' + f
    im = Image.open(filename)
    resize_images(filename, filename, (x,y))
    
    # F[name].export(filename, 600)     # set height to 600 pixels
