try:
    import os
    import json
    import logging
except Exception as e:
    print("E001", e)
    input()
    quit()
try:
    import numpy as np
except Exception as e:
    print("E024", e)
    input()
    quit()
try:
    import utils
except Exception as e:
    print("E025", e)
    input()
    quit()
try:
    from PIL import Image
except Exception as e:
    print("E008", e)
    input()
    quit()
try:
    from tqdm import tqdm
except Exception as e:
    print("E026", e)
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
    print("E003", e)
    input()
    quit()


#def tanh(num):
#    return (np.exp(num) - np.exp(-num)) / (np.exp(num) + np.exp(-num))

def sigmoid(num):
    return 1 / (1 + np.exp(-num))
    #return num


def Start(inp_const, weight, Xshape, directoryOut, bias, weights_hidden_to_output, bias_hidden_to_output, Yshape, weights_input_to_hidden):
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    tqdmrange = tqdm(range(len(inp_const)*len(letters)))
    for stLetter in range(len(inp_const)):
        for letter in range(len(letters)):
            tqdmrange.update()
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
            #print(pred)
            #pred = (pred - pred.min())/(pred.max() - pred.min()).reshape((Xshape, int(np.shape(weight[len(weight)-1])[1]/Xshape)))
            #pred2 = np.array([])
            #for i in pred:
            #    #print(i[0])
            #    pred2 = np.append(pred2, i[0])
            ##print(pred2)
            #pred2 = pred2.reshape((Xshape, Xshape))
            ##plt.imshow(pred2, interpolation='nearest')
            ##plt.show()
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
    
try:
    language = utils.load_language()
    try:
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_png')
        directoryModel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
        if not os.path.exists(directoryModel):
            os.makedirs(directoryModel)
        directoryOut = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_main')
        if not os.path.exists(directoryOut):
            os.makedirs(directoryOut)
    except Exception as err:
        logger.error("E006",exc_info=True)
        input()
        quit()
    try:
        files = os.listdir(directory)
        filesModel = os.listdir(directoryModel)
    except Exception as err:
        logger.error("E015",exc_info=True)
        input()
        quit()
    while True:
        try:
            strq=language["SelectFont"]
            for i in range(len(files)):
                strq += '[' + str(i) + ']' + files[i] + '\n'
            strq += '>>>'
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
            print(language["ErrorNumber"])
    while True:
        try:
            strq=language["SelectModel"]
            for i in range(len(filesModel)):
                strq += '[' + str(i) + ']' + filesModel[i] + '\n'
            strq += '>>>'
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
            print(language["ErrorNumber"])
    try:
        files = os.listdir(directory)
    except Exception as err:
        logger.error("E015",exc_info=True)
        input()
        quit()
    inp, weight, bias, weights_hidden_to_output, bias_hidden_to_output, Xshape, Yshape, weights_input_to_hidden = utils.load_dataset(directory, files, directoryModel)
    #print(type(weight[1]))
    Start(inp, weight, Xshape, directoryOut, bias, weights_hidden_to_output, bias_hidden_to_output, Yshape, weights_input_to_hidden)
    print(language["program_End"])
    logger.debug('Program End')
    input()
except Exception as err:
    logger.error('E000',exc_info=True)
    input()
