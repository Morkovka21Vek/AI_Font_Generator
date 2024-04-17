try:
    import logging
    import os
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "other","logs")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "other", "logs"))
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "other", "logs", "settings_log.log"),filemode="w",format="%(asctime)s %(levelname)s %(message)s")
except Exception as e:
    print("E003", e)
    input()
    quit()
try:
    import json
    from colorama import Fore
    import colorama 
    from tqdm import tqdm
    import requests
    colorama.init()
except Exception as e:
    logging.error("E001",exc_info=True)
    print("E001")
    input()
    quit()
    
    
def createJson(skip):
    directoryToOther = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'other')
    logging.debug("Directory other: "+directoryToOther)
    languages = os.listdir(os.path.join(directoryToOther, 'languages'))
    while True:
        try:
            strq=''
            for i in range(len(languages)):
                with open(os.path.join(directoryToOther, 'languages', languages[i]), encoding='utf-8') as f:
                    text = json.load(f)['ChooseLanguage']
                strq += '[' + Fore.GREEN + languages[i].removesuffix('.json') + Fore.RESET + ']' + text + '\n'
            #strq += '>>>'
        except Exception as err:
            logging.error('E012',exc_info=True)
            print(Fore.RED+language["Exception"].format("E012")+Fore.RESET)
            input()
            quit()
        print(strq, end='')
        try:
            inp = input('>>>').upper()
            logging.info(inp)
        except Exception as err:
            logging.error('E013',exc_info=True)
            print(Fore.RED+language["Exception"].format("E013")+Fore.RESET)
            input()
            quit()
        if inp == '' and skip == True:
            logging.info("return language select")
            return

        if inp+'.json' in languages:
            #languages.index(inp+'.json')
            with open(os.path.join(directoryToOther, 'languages', inp+'.json'), encoding='utf-8') as f:
                textFileLanguage = json.load(f)
            textFile={}
            textFile["Language"] = textFileLanguage
            textFile["Settings"]={}
            textFile["Settings"]["version"] = "0.5.0"
            textFile["Settings"]["modelVersion"] = 1
            textFile["Settings"]["modelPixelsImg"] = [35, 35]
            textFile["Settings"]["linkToConfig"] = "https://huggingface.co/Morkovka21Vek/AI_Font_Generator/raw/main/config.json"
            file = json.dumps(textFile, ensure_ascii=False, indent=4)
            directoryToTrain = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'training')
            logging.info("Directory Train(for json): "+directoryToTrain)
            with open(os.path.join(directoryToTrain, 'settings.json'), 'w', encoding='utf-8') as f:
                f.write(file)
            logging.info("Train file save")
            directoryToUsage = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usage')
            logging.info("Directory Usage(for json): "+directoryToUsage)
            with open(os.path.join(directoryToUsage, 'settings.json'), 'w', encoding='utf-8') as f:
                f.write(file)
            logging.info("Usage file save")
            with open(os.path.join(directoryToOther, 'settings.json'), 'w', encoding='utf-8') as f:
                f.write(file)
            logging.info("Other file save")
            return
        else:
            logging.warning('E014')
            strq=''
            for i in range(len(languages)):
                with open(os.path.join(directoryToOther, 'languages', languages[i]), encoding='utf-8') as f:
                    text = json.load(f)['LanguageError']
                strq += '[' + Fore.RED + languages[i].removesuffix('.json') + Fore.RESET + ']' + text + '\n'
            print(strq)
            
def loadModels(settings, language):
    try:
        response = requests.get(settings["linkToConfig"])
    except Exception as err:
        logging.warning("E034",exc_info=True)
        print(Fore.RED + language['ErrorConnect'] + Fore.RESET)
        return
    logging.info(response.status_code)
    if not response.status_code == 200:
        logging.warning("E034")
        print(Fore.RED + language['ErrorConnect'] + Fore.RESET)
        return
    remoteModelsAll = response.json()["models"]
    remoteModels=[]
    for i in remoteModelsAll:
        if i["modelVersion"] == settings["modelVersion"]:
            remoteModels.append(i)
    while True:
        try:
            strq=language["SelectModel"]
            for i in range(len(remoteModels)):
                strq += '[' + Fore.GREEN + str(i) + Fore.RESET + ']' + remoteModels[i]["name"] +' ('+remoteModels[i]["date"]+')'+ '\n'
            if len(remoteModels) == 0:
                print(Fore.YELLOW+language["NoModelsToVersion"]+Fore.RESET)
                return
        except Exception as err:
            logging.error("E012",exc_info=True)
            print(Fore.RED+language["Exception"].format("E012")+Fore.RESET)
            input()
            quit()
        print(strq,end='')
        remoteModelsStr = input('>>>')
        logging.info(remoteModelsStr)
        if remoteModelsStr == '':
            return
        try:
            remoteModelsNum = int(remoteModelsStr)
        except Exception as err:
            logging.error("E013",exc_info=True)
            print(Fore.RED+language["Exception"].format("E013")+Fore.RESET)
            input()
            quit()
        if remoteModelsNum >= 0 and remoteModelsNum < len(remoteModels):
            break
        else:
            logging.warning('E014')
            print(Fore.RED+language["ErrorNumber"]+Fore.RESET)
    try:
        responseModel = requests.get(remoteModels[remoteModelsNum]["url"], stream=True)
        total_size = int(responseModel.headers.get("content-length", 0))
        block_size = 1024
        logging.debug(total_size)
    except Exception as err:
        logging.warning("E034",exc_info=True)
        print(Fore.RED + language['ErrorConnect'] + Fore.RESET)
        return
    if not responseModel.status_code == 200:
        logging.warning("E034")
        print(Fore.RED + language['ErrorConnect'] + Fore.RESET)
        return
    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usage', 'models', remoteModels[remoteModelsNum]["name"]+'.'+remoteModels[remoteModelsNum]["extension"]), "wb") as file:
            for data in responseModel.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
    if total_size != 0 and progress_bar.n != total_size:
        logging.error("Could not download file")
    #with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', remoteModels[remoteModelsNum]["fullname"]), 'wb') as f:
    #    f.write(responseModel.content)

try:
    directory = os.path.dirname(os.path.abspath(__file__))
    logging.debug("Directory: "+directory)
    if not os.path.exists(os.path.join(directory, 'training', 'input')):
        os.makedirs(os.path.join(directory, 'training', 'input'))
    logging.debug("create folder input done")
    directoryModel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usage', 'models')
    logging.debug("Directory model: "+directoryModel)
    if not os.path.exists(directoryModel):
        os.makedirs(directoryModel)
    logging.debug("create folder model done")
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'other', 'settings.json')):
        logging.info("No found settings.json in other")
        createJson(False)
        logging.info("createJson returned")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'other', 'settings.json'), encoding='utf-8') as f:
        fileJson = json.load(f)
        language = fileJson["Language"]
        settings = fileJson["Settings"]
    logging.info("settings.json load")
    while True:
        print(language["SelectAction"].format(Fore.GREEN+"0"+Fore.RESET, Fore.GREEN+"1"+Fore.RESET))
        inp = input('>>>')
        logging.debug(inp)
        if inp == '0':
            createJson(True)
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'other', 'settings.json'), encoding='utf-8') as f:
                fileJson = json.load(f)
                language = fileJson["Language"]
                settings = fileJson["Settings"]
            logging.info("settings.json load")
        elif inp == '1':
            loadModels(settings, language)
        elif inp == '':
            logging.info("quit")
            quit()
        else:
            logging.warning('E014')
            print(Fore.YELLOW+language["ErrorNumber"]+Fore.RESET)
 
    #input(Fore.GREEN + language["program_End"] + Fore.RESET)
    #quit()
except Exception as err:
    logging.error('E000',exc_info=True)
    print(Fore.RED+language["Exception"].format("E000")+Fore.RESET)
    input()