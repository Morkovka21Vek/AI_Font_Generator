import os
import json
import traceback
import sys
try:
    import fontforge
except:
    #print(sys.executable.split("\\")[-1])
    if not sys.executable.split("\\")[-1] == "ffpython.exe":
        with open(os.path.abspath(os.getcwd())+'\\settings.json', encoding='utf-8') as f:
            settings = json.load(f)["Settings"]
        #print('cd '+settings["directoryToAI_Font_Generator"]+'\\training', settings["directoryToFFpython"])
        os.system(settings["directoryToFFpython"])
        os.system('cd '+settings["directoryToAI_Font_Generator"]+'\\usage')
        quit()
    else:
        with open(os.path.abspath(os.getcwd())+'\\settings.json', encoding='utf-8') as f:
            language = json.load(f)["Language"]
        print(language["Exception"])
        traceback.print_exc()
        input()
        quit()
try:
    with open(os.path.abspath(os.getcwd())+'\\settings.json', encoding='utf-8') as f:
        language = json.load(f)["Language"]
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
    print(language["Exception"])
    traceback.print_exc()
    input()