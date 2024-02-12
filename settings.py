import os
import json
import traceback
try:
    
    directory = os.path.abspath(os.getcwd())
    if not os.path.exists(directory + '\\training\\input'):
        os.makedirs(directory + '\\training\\input')
    if not os.path.exists(directory + '\\training\\output'):
        os.makedirs(directory + '\\training\\output')
    if not os.path.exists(directory + '\\training\\out_png'):
        os.makedirs(directory + '\\training\\out_png')

    if not os.path.exists(directory + '\\usage\\out_main'):
        os.makedirs(directory + '\\usage\\out_main')
    if not os.path.exists(directory + '\\usage\\output'):
        os.makedirs(directory + '\\usage\\output')
    if not os.path.exists(directory + '\\usage\\out_png'):
        os.makedirs(directory + '\\usage\\out_png')
    if not os.path.exists(directory + '\\usage\\out_svg'):
        os.makedirs(directory + '\\usage\\out_svg')

    directoryToOther = os.path.realpath('other')
    languages = os.listdir(directoryToOther + '\\languages')
    strq=''
    for i in range(len(languages)):
        with open(directoryToOther+'\\languages\\'+languages[i], encoding='utf-8') as f:
            text = json.load(f)['ChooseLanguage']
            #print(text)
        strq += '[' + languages[i].removesuffix('.json') + ']' + text + '\n'
    strq += '>>>'
    inp = input(strq)

    if inp+'.json' in languages:
        #languages.index(inp+'.json')
        with open(directoryToOther+'\\languages\\'+inp+'.json', encoding='utf-8') as f:
            textFileLanguage = json.load(f)
            textFile={}
            textFile["Language"] = textFileLanguage
            #file = json.dumps(textFile, indent=2, encoding='utf-8')
            directoryToFFpython = '"' + directoryToOther + '\\ffpython\\bin\\ffpython.exe" ttf2png.py'
            textFile["Settings"]={}
            textFile["Settings"]["directoryToAI_Font_Generator"] = directory
            textFile["Settings"]["directoryToFFpython"] = directoryToFFpython
            file = json.dumps(textFile, ensure_ascii=False, indent=4)
            directoryToTrain = os.path.realpath('training')
            with open(directoryToTrain+'\\settings.json', 'w', encoding='utf-8') as f:
                f.write(file)
            directoryToUsage = os.path.realpath('usage')
            with open(directoryToUsage+'\\settings.json', 'w', encoding='utf-8') as f:
                f.write(file)
                
            #directoryToFFpython = '"' + directoryToOther + '\\ffpython\\bin\\ffpython.exe" ttf2png.py'
            #with open(directoryToTrain+'\\start_ttf2png.bat', 'w', encoding='utf-8') as f:
            #    f.write(directoryToFFpython)
            #with open(directoryToUsage+'\\start_ttf2png.bat', 'w', encoding='utf-8') as f:
            #    f.write(directoryToFFpython)

            with open(directoryToOther+'\\languages\\'+inp+'.json', encoding='utf-8') as f:
                text = json.load(f)["Programm_End"]
            input(text)
            
    else:
        strq=''
        for i in range(len(languages)):
            with open(directoryToOther+'\\languages\\'+languages[i], encoding='utf-8') as f:
                text = json.load(f)['LanguageError']
            strq += '[' + languages[i].removesuffix('.json') + ']' + text + '\n'
        #print(strq)
        input(strq)
except Exception:
    strq=''
    for i in range(len(languages)):
        with open(directoryToOther+'\\languages\\'+languages[i], encoding='utf-8') as f:
            text = json.load(f)['Exception']
        strq += '[' + languages[i].removesuffix('.json') + ']' + text + '\n'
    print(strq)
    traceback.print_exc()
    input()
#with open('example.txt') as f:
