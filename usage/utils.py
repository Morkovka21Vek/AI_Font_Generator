try:
    import logging
    import os
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "utils_log.log"),filemode="w",format="%(asctime)s %(levelname)s %(message)s")
except Exception as e:
    print("E003", e)
    input()
    quit()
try:
    import json
    from PIL import Image
    import numpy as np
    from tqdm import tqdm
    from colorama import Fore
    from safetensors.numpy import load_file
except Exception as e:
    logging.error("E001",exc_info=True)
    print("E001")
    input()
    quit()
logging.debug("Import Done!")

def load_settings():
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
            settings = json.load(f)["Settings"]
        logging.debug("Import settings Done")
    except Exception as err:
        logging.error('E002',exc_info=True)
        print("E002")
        input()
        quit()
    return settings

def load_language():
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
            language = json.load(f)["Language"]
        logging.debug("Import language Done")
    except Exception as err:
        logging.error('E002',exc_info=True)
        print("E002")
        input()
        quit()
    return language

def load_dataset(directory, files, directoryModel):
    #letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    language = load_language()
    inp=[]
    weight=[]
    bias=[]
    for file in tqdm(files):
        try:
            img = Image.open(os.path.join(directory, file))
        except Exception as err:
            logging.error("E009",exc_info=True)
            print(Fore.RED+language["Exception"].format("E009")+Fore.RESET)
            input()
            quit()
        try:
            imageToMatrice = np.asarray(img)
        except Exception as err:
            logging.error("E020",exc_info=True)
            print(Fore.RED+language["Exception"].format("E020")+Fore.RESET)
            input()
            quit()
        inp.append(imageToMatrice.ravel())
    try:
        inp_np = np.array(inp)
    except Exception as err:
        logging.error("E021",exc_info=True)
        print(Fore.RED+language["Exception"].format("E021")+Fore.RESET)
        input()
        quit()
    #weight = np.load(directoryModel)
    try:
        weightData = load_file(directoryModel)#np.load(directoryModel)
    except Exception as err:
        logging.error("E022",exc_info=True)
        print(Fore.RED+language["Exception"].format("E022")+Fore.RESET)
        input()
        quit()
    try:
        for i in range(weightData['weightLen']):
            weight.append(weightData[f'weight{i+1}'])
        weights_hidden_to_output = weightData['weights_hidden_to_output']
        weights_input_to_hidden = weightData['weights_input_to_hidden']

        for i in range(weightData['biasLen']):
            bias.append(weightData[f'bias{i+1}'])
        bias_hidden_to_output = weightData['bias_hidden_to_output']

        Xshape = weightData['Xshape']
        Yshape = weightData['Yshape']
    except Exception as err:
        logging.error("E023",exc_info=True)
        print(Fore.RED+language["Exception"].format("E023")+Fore.RESET)
        input()
        quit()
    logging.info('ImportDone')
    return inp_np, weight, bias, weights_hidden_to_output, bias_hidden_to_output, Xshape, Yshape, weights_input_to_hidden
