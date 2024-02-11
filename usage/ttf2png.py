import fontforge
import os
import json
import traceback


try:
    with open(os.path.abspath(os.getcwd())+'\\language.json', encoding='utf-8') as f:
        language = json.load(f)
    fileinputname = input(language["InputFilePath"]).replace('"', '')
    #print(fileinputname)
    F = fontforge.open(fileinputname)
    filename = os.path.realpath('out_png') + '\\'
    filename = filename + os.path.splitext(os.path.basename(fileinputname))[0]
    if not os.path.exists(filename):
        os.makedirs(filename)
    for name in F:
        #print(filename + '\\' + name + '.png')
        F[name].export(filename + '\\' + name + '.png')
    print(language["Programm_End"])
    input()
except:
    input(language["Exception"], traceback.print_exc())