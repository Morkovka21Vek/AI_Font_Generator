try:
    import logging
    import os
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "main_log.log"),filemode="w",format="%(asctime)s %(levelname)s %(message)s")
except Exception as e:
    print("E003", e)
    input()
    quit()
try:
    import json
    import numpy as np
    from PIL import Image
    from tqdm import tqdm
    from colorama import Fore
except Exception as err:
    logging.error("E001",exc_info=True)
    print("E001")
    input()
    quit()
try:
    import utils
except Exception as e:
    logging.error("E025",exc_info=True)
    print(Fore.RED+"E025"+Fore.RESET)
    input()
    quit()

def sigmoid(num):
    return 1 / (1 + np.exp(-num))

def Start(inp_const, weight, Xshape, directoryOut, bias, weights_hidden_to_output, bias_hidden_to_output, Yshape, weights_input_to_hidden):
    letters = [ord(i) for i in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']]
    tqdmRange = tqdm(range(len(inp_const)*len(letters)))
    for stLetter in range(len(inp_const)):
        for letter in range(len(letters)):
            tqdmRange.update()
            try:
                hidden=[]
                inp = np.reshape(np.append(inp_const[stLetter], letter/(len(letters)-1)), (-1, 1))
                hidden.append(sigmoid(bias[0] + np.dot(weights_input_to_hidden, inp)))
                for i in range(len(weight)):
                    hidden.append(sigmoid(bias[i+1] + np.dot(weight[i], hidden[i-1])))
                pred = sigmoid(bias_hidden_to_output + np.dot(weights_hidden_to_output, hidden[-1]))
            except Exception as err:
                logging.error("E027",exc_info=True)
                print(Fore.RED+language["Exception"].format("E017")+Fore.RESET)
                input()
                quit()
            try:
                pred = pred.reshape((Xshape, Yshape))
            except Exception as err:
                logging.error("E018",exc_info=True)
                print(Fore.RED+language["Exception"].format("E018")+Fore.RESET)
                input()
                quit()
            try:
                im = Image.fromarray(pred*255)
                im = im.convert('RGB')
            except Exception as err:
                logging.error("E028",exc_info=True)
                print(Fore.RED+language["Exception"].format("E028")+Fore.RESET)
                input()
                quit()
            try:
                im.save(os.path.join(directoryOut, str(stLetter) + '.' + letters[letter] + '.png', format='PNG'))
            except Exception as err:
                logging.error("E017",exc_info=True)
                print(Fore.RED+language["Exception"].format("E017")+Fore.RESET)
                input()
                quit()
                
try:
    language = utils.load_language()
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_png')
    logging.debug("Out_png dir: "+directory)
    directoryModel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    logging.debug("Models dir: "+directoryModel)
    if not os.path.exists(directoryModel):
        os.makedirs(directoryModel)
    directoryOut = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_main')
    logging.debug("Out_main dir: "+directoryOut)
    if not os.path.exists(directoryOut):
        os.makedirs(directoryOut)
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
        except Exception as err:
            logging.error("E012",exc_info=True)
            print(Fore.RED+language["Exception"].format("E012")+Fore.RESET)
            input()
            quit()
        try:
            print(strq, end='')
            num = int(input(">>>"))
            logging.info(num)
        except Exception as err:
            logging.error("E013",exc_info=True)
            print(Fore.RED+language["Exception"].format("E013")+Fore.RESET)
            input()
            quit()
        if num >= 0 and num < len(files):
            directory = os.path.join(directory, files[num])
            logging.debug(directory)
            break
        else:
            logging.warning('E014')
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
        except Exception as err:
            logging.error("E012",exc_info=True)
            print(Fore.RED+language["Exception"].format("E012")+Fore.RESET)
            input()
            quit()
        try:
            print(strq, end='')
            numModel = int(input('>>>'))
            logging.info(numModel)
        except Exception as err:
            logging.error("E013",exc_info=True)
            print(Fore.RED+language["Exception"].format("E013")+Fore.RESET)
            input()
            quit()
        if numModel >= 0 and numModel < len(filesModel):
            directoryModel = os.path.join(directoryModel, filesModel[numModel])
            logging.debug(directoryModel)
            break
        else:
            logging.warning('E014(model)')
            print(Fore.RED+language["ErrorNumber"]+Fore.RESET)
    files = os.listdir(directory)
    inp, weight, bias, weights_hidden_to_output, bias_hidden_to_output, Xshape, Yshape, weights_input_to_hidden = utils.load_dataset(directory, files, directoryModel)
    print(Fore.GREEN+language["ImportDone"]+Fore.RESET)
    Start(inp, weight, Xshape, directoryOut, bias, weights_hidden_to_output, bias_hidden_to_output, Yshape, weights_input_to_hidden)
    print(Fore.GREEN+language["program_End"]+Fore.RESET)
    logging.debug('Program End')
    input()
except Exception as err:
    logging.error('E000',exc_info=True)
    input()
