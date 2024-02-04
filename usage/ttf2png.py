import fontforge
import os

fileinputname = input('Введите пожалуйста путь к файлу шрифта(можно перетащить): >>>').replace('"', '')
#print(fileinputname)
F = fontforge.open(fileinputname)
filename = os.path.realpath('out_png') + '\\'
filename = filename + os.path.splitext(os.path.basename(fileinputname))[0]
if not os.path.exists(filename):
    os.makedirs(filename)
for name in F:
    #print(filename + '\\' + name + '.png')
    F[name].export(filename + '\\' + name + '.png')
