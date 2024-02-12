import os
import json
import sys
try:
    #print(sys.executable.split("\\")[-1])
    import fontforge
except:
    #print(sys.executable.split("\\")[-1])
    if not sys.executable.split("\\")[-1] == "ffpython.exe":
        with open(os.path.abspath(os.getcwd())+'\\settings.json', encoding='utf-8') as f:
            settings = json.load(f)["Settings"]
        #print('cd '+settings["directoryToAI_Font_Generator"]+'\\training', settings["directoryToFFpython"])
        os.system(settings["directoryToFFpython"])
        os.system('cd '+settings["directoryToAI_Font_Generator"]+'\\training')
    quit()
    #input()
#"C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" ttf2png.py
with open(os.path.abspath(os.getcwd())+'\\settings.json', encoding='utf-8') as f:
    language = json.load(f)["Language"]

directory = os.path.realpath('input')
files = os.listdir(directory)
directoryOut = os.path.realpath('out_png')
strq=''
for i in range(len(files)):
    strq += '[' + str(i) + ']' + files[i] + '\n'
print(strq)
nach=int(input(language["Start_s"]))
kon=int(input(language["End"]))
for i in range(nach, kon+1):
    fileinputname = directory + '\\' + files[i]# + '.ttf'
    print(fileinputname)
    F = fontforge.open(fileinputname)
    for name in F:
        #filename = "C:\\Users\\User\\Desktop\\Training\\" + str(i) + "." + name + ".png"
        filename = directoryOut + '\\' + str(i) + "." + name + ".png"
        #filename = "C:\\Users\\User\\Desktop\\789\\" + name + ".png"
        # print name
        #path = "C:\\Users\\User\\Desktop\\789\\" + str(i) + "\\"
        #if not os.path.exists(path):
        #    os.makedirs(path)
        #print(filename)
        F[name].export(filename)
    #print('Экспорт ', fileinputname, ' завершён!', '(', i, ')')
    print(language["Export_end"]. format(fileinputname, i))
        # F[name].export(filename, 600)     # set height to 600 pixels
