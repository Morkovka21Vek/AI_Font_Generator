try:
    import os
    import json
    from random import randint
    from copy import deepcopy
    import logging
    import numpy as np
    from PIL import Image
    from tqdm import tqdm
except Exception as e:
    print("E001(utils)", e)
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

try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
        language = json.load(f)["Language"]
    logger.debug("Import language Done")
except Exception as err:
    logger.error('E002(utils)',exc_info=True)
    input()
    quit()

#def find(s, ch):
#    return [i for i, ltr in enumerate(s) if ltr == ch]

def sort_by_indexes(lst, indexes, reverse=False):
  return [val for (_, val) in sorted(zip(indexes, lst), key=lambda x: \
          x[0], reverse=reverse)]

def shuffle(lst):
  temp_lst = deepcopy(lst)
  m = len(temp_lst)
  while (m):
    m -= 1
    i = randint(0, m)
    temp_lst[m], temp_lst[i] = temp_lst[i], temp_lst[m]
  return temp_lst

def load_dataset():
    try:
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_png')
        letters = [ord(i) for i in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']]
        numbers = []
        files = os.listdir(directory)
        goal_pred=[]
        inp=[]
        x_train=[]
        y_train=[]
        font=0
        logger.info("1/4")
        for file in tqdm(files):
            img = Image.open(os.path.join(directory, file))
            imageToMatrice = np.asarray(img)

            
            strF = file.removesuffix('.png')
            result_str = ''
            for iF in range(len(strF)): 
                if iF > strF.index('.'): 
                    result_str = result_str + strF[iF] 
            #y_train.append(result_str)

            result_str2 = ''
            for iF in range(len(strF)): 
                if iF < strF.index('.'): 
                    result_str2 = result_str2 + strF[iF] 
            #z_train.append(result_str2)
            #z_train = result_str2
            
            #print(strF,result_str2)
            
            #find(result_str2, font)

            if not result_str2 in numbers:
                x_train.append([])
                y_train.append([])
                numbers.append(result_str2)
                
            #x_train[numbers.index(result_str2)].append(imageToMatrice.astype("float32") / 255)
            x_train[numbers.index(result_str2)].append(imageToMatrice.astype(np.float32) / 255)
            if result_str.lower() in letters:
                y_train[numbers.index(result_str2)].append(letters.index(result_str.lower()))
            else:
                y_train[numbers.index(result_str2)].append(-1)

        logger.info("2/4")
        for i1 in tqdm(range(len(x_train))):
            for i2 in range(len(x_train[i1])):
                if y_train[i1][i2] != -1:
                    for i3 in range(len(x_train[i1])):
                        #np.append(inp, x_train[i1][i3])
                        #np.append(inp, np.append(x_train[i1][i3], y_train[i1][i2]))
                        #np.append(goal_pred, x_train[i1][i2])
                        inp.append(np.append(x_train[i1][i3], y_train[i1][i2]/(len(letters)-1)))
                        goal_pred.append(x_train[i1][i2])

        #inp_np = np.array(inp)
        #goal_pred_np = np.array(goal_pred)
        
        #return x_train, y_train
        w = []
        z = []
        logger.info("3/4")
        for i in tqdm(range(len(inp))):
            w.append(np.reshape(inp[i].ravel(), (-1, 1)).astype(np.float32))
            z.append(np.reshape(goal_pred[i].ravel(), (-1, 1)).astype(np.float32))
        #inp = np.array(w)
        #goal_pred = np.array(z)
        numbers = np.arange(len(w))
        numbers = shuffle(numbers)
        #print(sort_by_indexes(w, numbers))
        inp = np.array(sort_by_indexes(w, numbers))
        goal_pred = np.array(sort_by_indexes(z, numbers))
        
        logger.info("4/4")
        logger.debug("ImportDone")
        print(language["ImportDone"])
    except Exception as err:
        logger.error('E000',exc_info=True)
        input()
    return inp, goal_pred
