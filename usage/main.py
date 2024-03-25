try:
    import os
    import json
    import logging
    import numpy as np
    from PIL import Image
    from tqdm import tqdm
    from colorama import Fore
    import requests
except Exception as e:
    try:
        print(Fore.RED+"E001"+Fore.RESET, e)#Fore.RED+language["ErrorNumber"]+Fore.RESET
    except:
        print("E001", e)
    input()
    quit()
try:
    import utils
except Exception as e:
    print(Fore.RED+"E025"+Fore.RESET, e)
    input()
    quit()
try:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "main_log.log"), mode='w')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
except Exception as e:
    print(Fore.RED+"E003"+Fore.RESET, e)
    input()
    quit()


#def tanh(num):
#    return (np.exp(num) - np.exp(-num)) / (np.exp(num) + np.exp(-num))

def sigmoid(num):
    return 1 / (1 + np.exp(-num))
    #return num


def Start(inp_const, weight, Xshape, directoryOut, bias, weights_hidden_to_output, bias_hidden_to_output, Yshape, weights_input_to_hidden):
    letters = [ord(i) for i in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']]
    tqdmRange = tqdm(range(len(inp_const)*len(letters)))
    for stLetter in range(len(inp_const)):
        for letter in range(len(letters)):
            tqdmRange.update()
            #inp = np.reshape(inp_const[stLetter], (-1, 1))
            #layers=[]
            #layers.append(np.dot(np.append(inp, letter), weight[0]))
            #pred = (pred - pred.min())/(pred.max() - pred.min()).reshape((Xshape, int(np.shape(weight[len(weight)-1])[1]/Xshape)))
            try:
                hidden=[]
                inp = np.reshape(np.append(inp_const[stLetter], letter/(len(letters)-1)), (-1, 1))
                #hidden.append(sigmoid(bias[0] + np.dot(weight[0], np.append(inp_const[0], letter/len(letters)-1))))
                hidden.append(sigmoid(bias[0] + np.dot(weights_input_to_hidden, inp)))
                for i in range(len(weight)):
                    hidden.append(sigmoid(bias[i+1] + np.dot(weight[i], hidden[i-1])))
                pred = sigmoid(bias_hidden_to_output + np.dot(weights_hidden_to_output, hidden[-1]))
            except Exception as err:
                logger.error("E027",exc_info=True)
                input()
                quit()
            try:
                pred = pred.reshape((Xshape, Yshape))
            except Exception as err:
                logger.error("E018",exc_info=True)
                input()
                quit()
            try:
                im = Image.fromarray(pred*255)
                im = im.convert('RGB')
            except Exception as err:
                logger.error("E028",exc_info=True)
                input()
                quit()
            try:
                im.save(os.path.join(directoryOut, str(stLetter) + '.' + letters[letter] + '.png', format='PNG'))
            except Exception as err:
                logger.error("E017",exc_info=True)
                input()
                quit()
                
def loadModels(settings, language):
    try:
        response = requests.get(settings["linkToConfig"])
    except Exception as err:
        logger.warning("E034",exc_info=True)
        print(Fore.RED + language['ErrorConnect'] + Fore.RESET)
        return
    logger.info(response.status_code)
    if not response.status_code == 200:
        logger.warning("E034")
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
                strq += '[' + Fore.GREEN + str(i) + Fore.RESET + ']' + remoteModels[i]["name"] + '\n'
            if len(remoteModels) == 0:
                print(Fore.YELLOW+language["NoModelsToVersion"]+Fore.RESET)
                return
            else:
                strq += Fore.GREEN+'>>>'+Fore.RESET
        except Exception as err:
            logger.error("E012",exc_info=True)
            input()
            quit()
        try:
            remoteModelsNum = int(input(strq))
        except Exception as err:
            logger.error("E013",exc_info=True)
            input()
            quit()
        if remoteModelsNum >= 0 and remoteModelsNum < len(remoteModels):
            break
        else:
            logger.warning('E014')
            print(Fore.RED+language["ErrorNumber"]+Fore.RESET)
    try:
        responseModel = requests.get(remoteModels[remoteModelsNum]["link"], stream=True)
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        
    except Exception as err:
        logger.warning("E034",exc_info=True)
        print(Fore.RED + language['ErrorConnect'] + Fore.RESET)
        return
    if not responseModel.status_code == 200:
        logger.warning("E034")
        print(Fore.RED + language['ErrorConnect'] + Fore.RESET)
        return
    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', remoteModels[remoteModelsNum]["fullname"]), "wb") as file:
            for data in responseModel.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
    if total_size != 0 and progress_bar.n != total_size:
        logger.error("Could not download file")
    #with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', remoteModels[remoteModelsNum]["fullname"]), 'wb') as f:
    #    f.write(responseModel.content)
    
try:
    language = utils.load_language()
    settings = utils.load_settings()
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_png')
    directoryModel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    if not os.path.exists(directoryModel):
        os.makedirs(directoryModel)
    directoryOut = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_main')
    if not os.path.exists(directoryOut):
        os.makedirs(directoryOut)
    inpDownload = input(language["downloadOrContinue"]+Fore.GREEN+' >>>'+Fore.RESET)
    if inpDownload == '1':
        loadModels(settings, language)
    files = os.listdir(directory)
    filesModel = os.listdir(directoryModel)
    while True:
        try:
            strq=language["SelectFont"]
            for i in range(len(files)):
                strq += '[' + Fore.GREEN + str(i) + Fore.RESET + ']' + files[i] + '\n'
            if len(files) == 0:
                print(strq+Fore.RED+language["EmptyListWithEnter"]+Fore.RESET)
                input()
                quit()
            else:
                strq += Fore.GREEN+'>>>'+Fore.RESET
        except Exception as err:
            logger.error("E012",exc_info=True)
            input()
            quit()
        try:
            num = int(input(strq))
        except Exception as err:
            logger.error("E013",exc_info=True)
            input()
            quit()
        if num >= 0 and num < len(files):
            directory = os.path.join(directory, files[num])
            logger.debug(directory)
            break
        else:
            logger.warning('E014')
            print(Fore.RED+language["ErrorNumber"]+Fore.RESET)
    while True:
        try:
            strq=language["SelectModel"]
            for i in range(len(filesModel)):
                strq += '[' + Fore.GREEN + str(i) + Fore.RESET + ']' + filesModel[i] + '\n'
            if len(filesModel) == 0:
                print(strq+Fore.RED+language["EmptyListWithEnter"]+Fore.RESET)
                input()
                quit()
            else:
                strq += Fore.GREEN+'>>>'+Fore.RESET
        except Exception as err:
            logger.error("E012",exc_info=True)
            input()
            quit()
        try:
            numModel = int(input(strq))
        except Exception as err:
            logger.error("E013",exc_info=True)
            input()
            quit()
        if numModel >= 0 and numModel < len(filesModel):
            directoryModel = os.path.join(directoryModel, filesModel[numModel])
            logger.debug(directoryModel)
            break
        else:
            logger.error('E014(model)')
            print(Fore.RED+language["ErrorNumber"]+Fore.RESET)
    files = os.listdir(directory)
    inp, weight, bias, weights_hidden_to_output, bias_hidden_to_output, Xshape, Yshape, weights_input_to_hidden = utils.load_dataset(directory, files, directoryModel)
    print(Fore.GREEN+language["ImportDone"]+Fore.RESET)
    Start(inp, weight, Xshape, directoryOut, bias, weights_hidden_to_output, bias_hidden_to_output, Yshape, weights_input_to_hidden)
    print(Fore.GREEN+language["program_End"]+Fore.RESET)
    logger.debug('Program End')
    input()
except Exception as err:
    logger.error('E000',exc_info=True)
    input()
