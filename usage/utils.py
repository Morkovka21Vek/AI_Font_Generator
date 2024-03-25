try:
    import os
    import json
    import logging
    from PIL import Image
    import numpy as np
    from tqdm import tqdm
    from colorama import Fore
except Exception as e:
    try:
        print(Fore.RED+"E001"+Fore.RESET, e)
    except:
        print("E001", e)
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
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "utils_log.log"), mode='w')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
except Exception as e:
    print(Fore.RED+"E003"+Fore.RESET, e)
    input()
    quit()

logger.debug("Import Done!")

def load_settings():
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
            settings = json.load(f)["Settings"]
        logger.debug("Import settings Done")
    except Exception as err:
        logger.error('E002(settings)',exc_info=True)
        input()
        quit()
    return settings

def load_language():
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
            language = json.load(f)["Language"]
        logger.debug("Import language Done")
    except Exception as err:
        logger.error('E002(utils)',exc_info=True)
        input()
        quit()
    return language

def load_dataset(directory, files, directoryModel):
    #letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    inp=[]
    weight=[]
    bias=[]
    for file in tqdm(files):
        try:
            img = Image.open(os.path.join(directory, file))
        except Exception as err:
            logger.error("E009",exc_info=True)
            input()
            quit()
        try:
            imageToMatrice = np.asarray(img)
        except Exception as err:
            logger.error("E020",exc_info=True)
            input()
            quit()
        inp.append(imageToMatrice.ravel())
    try:
        inp_np = np.array(inp)
    except Exception as err:
        logger.error("E021",exc_info=True)
        input()
        quit()
    #weight = np.load(directoryModel)
    try:
        weightData = np.load(directoryModel)
    except Exception as err:
        logger.error("E022",exc_info=True)
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
        logger.error("E023",exc_info=True)
        input()
        quit()
    logger.info('ImportDone')
    return inp_np, weight, bias, weights_hidden_to_output, bias_hidden_to_output, Xshape, Yshape, weights_input_to_hidden
