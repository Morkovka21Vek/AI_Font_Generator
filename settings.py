try:
    import os
    import json
    import logging
except Exception as e:
    print("E001", e)
    input()
    quit()

#try:
#    from colorama import Fore
#except Exception as e:
#    print("E030", e)
#    input()
#    quit()

try:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "other", "logs")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "other", "logs"))
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "other", "logs", "settings_log.log"), mode='w')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
except Exception as e:
    print("E003", e)
    input()
    quit()

try:
    directory = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(directory, 'training', 'input')):
        os.makedirs(os.path.join(directory, 'training', 'input'))
    if not os.path.exists(os.path.join(directory, 'training', 'output')):
        os.makedirs(os.path.join(directory, 'training', 'output'))
    if not os.path.exists(os.path.join(directory, 'training', 'out_png')):
        os.makedirs(os.path.join(directory, 'training', 'out_png'))
    if not os.path.exists(os.path.join(directory, 'training', 'log')):
        os.makedirs(os.path.join(directory, 'training', 'log'))

    if not os.path.exists(os.path.join(directory, 'usage', 'models')):
        os.makedirs(os.path.join(directory, 'usage', 'models'))

    logger.debug("create folders done")
    
    directoryToOther = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'other')
    languages = os.listdir(os.path.join(directoryToOther, 'languages'))
    while True:
        try:
            strq=''
            for i in range(len(languages)):
                with open(os.path.join(directoryToOther, 'languages', languages[i]), encoding='utf-8') as f:
                    text = json.load(f)['ChooseLanguage']
                strq += '[' + languages[i].removesuffix('.json') + ']' + text + '\n'
            strq += '>>>'
        except Exception as err:
                logger.error('E012',exc_info=True)
                input()
                quit()
        try:
            inp = input(strq).upper()
        except Exception as err:
                logger.error('E013',exc_info=True)
                input()
                quit()

        if inp+'.json' in languages:
            #languages.index(inp+'.json')
            with open(os.path.join(directoryToOther, 'languages', inp+'.json'), encoding='utf-8') as f:
                textFileLanguage = json.load(f)
                textFile={}
                textFile["Language"] = textFileLanguage
                #file = json.dumps(textFile, indent=2, encoding='utf-8')
                #directoryToFFpython = '"' + directoryToOther + '\\ffpython\\bin\\ffpython.exe" ttf2png.py'
                textFile["Settings"]={}
                #textFile["Settings"]["directoryToAI_Font_Generator"] = directory
                #textFile["Settings"]["directoryToFFpython"] = directoryToFFpython
                textFile["Settings"]["version"] = "0.4.0"
                textFile["Settings"]["modelVersion"] = "1"
                file = json.dumps(textFile, ensure_ascii=False, indent=4)
                directoryToTrain = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'training')
                with open(os.path.join(directoryToTrain, 'settings.json'), 'w', encoding='utf-8') as f:
                    f.write(file)
                directoryToUsage = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usage')
                with open(os.path.join(directoryToUsage, 'settings.json'), 'w', encoding='utf-8') as f:
                    f.write(file)
                    
                with open(os.path.join(directoryToOther, 'languages', inp+'.json'), encoding='utf-8') as f:
                    text = json.load(f)["program_End"]
                input(text)
                quit()
        else:
            logger.warning('E014')
            strq=''
            for i in range(len(languages)):
                with open(os.path.join(directoryToOther, 'languages', languages[i]), encoding='utf-8') as f:
                    text = json.load(f)['LanguageError']
                strq += '[' + languages[i].removesuffix('.json') + ']' + text + '\n'
            #print(strq)
            print(strq)
except Exception as err:
    logger.error('E000',exc_info=True)
    input()