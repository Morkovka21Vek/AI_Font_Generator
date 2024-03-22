try:
    import os
    import json
    import logging
except Exception as e:
    print("E001(utils)", e)
    input()
    quit()
try:
    from PIL import Image
except Exception as e:
    print("E008(utils)", e)
    input()
    quit()
try:
    import numpy as np
except Exception as e:
    print("E024(utils)", e)
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
    print("E003(utils)", e)
    input()
    quit()

logger.debug("Import Done!")

def load_language():
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
            language = json.load(f)
        logger.debug("Import language Done")
    except Exception as err:
        logger.error('E002(utils)',exc_info=True)
        input()
        quit()
    return language

def load_dataset(directory, files, directoryModel):
    #letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    inp=[]
    Xshape = 0
    weight=[]
    bias=[]
    for file in files:
        try:
            img = Image.open(os.path.join(directory, file))
        except Exception as err:
            logger.error("E009(utils)",exc_info=True)
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
    
    #biasData = np.load(directoryModel.removesuffix('.npz') + '_bias.npz')
    #for i in range(len(biasData)-1):
    #    #print(len(biasData), f'bias{i+1}')
    #    bias.append(biasData[f'bias{i+1}'])
    #bias_hidden_to_output = biasData['bias_hidden_to_output']
    #Xshape = weight[0]
    #np.delete(weight, 0)
        #strF = file.removesuffix('.png')
        #result_str = ''
        #for iF in range(len(strF)): 
        #    if iF > strF.index('.'): 
        #        result_str = result_str + strF[iF]

            
        #x_train[numbers.index(result_str2)].append(imageToMatrice.astype("float32") / 255)
        #if result_str.lower() in letters:
        #    y_train[numbers.index(result_str2)].append(letters.index(result_str.lower()))
        #else:
        #     y_train[numbers.index(result_str2)].append(-1)

    #for i1 in range(len(x_train)):
    #    for i2 in range(len(x_train[i1])):
    #        if y_train[i1][i2] != -1:
    #            for i3 in range(len(x_train[i1])):
    #                inp.append(np.append(x_train[i1][i3], y_train[i1][i2]))
    #                goal_pred.append(x_train[i1][i2])

    #inp_np = np.array(inp)
    #goal_pred_np = np.array(goal_pred)
    
    #return x_train, y_train
    #w = []
    #z = []
    #for i in range(len(inp)):
    #    w.append(inp[i].ravel())
    #    #z.append(goal_pred[i].ravel())
    #inp = np.array(w)
    #goal_pred = np.array(z)
    #print('ImportDone')
    logger.info('ImportDone')
    return inp_np, weight, bias, weights_hidden_to_output, bias_hidden_to_output, Xshape, Yshape, weights_input_to_hidden
