import os
import numpy as np
from PIL import Image
from copy import deepcopy
from random import randint
import json

with open(os.path.abspath(os.getcwd())+'\\language.json', encoding='utf-8') as f:
    language = json.load(f)

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
    directory = os.path.realpath('out_png')
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    numbers = []
    files = os.listdir(directory)
    #print(files)
    #goal_pred=np.array([])
    #inp=np.array([])
    goal_pred=[]
    inp=[]
    x_train=[]
    y_train=[]
    #train=[]
    #train2=[]
    font=0
    for file in files:
        img = Image.open(directory + '\\' + file)
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

    
        #if font == result_str2:
        #    train.append(imageToMatrice.astype("float32") / 255)
        #    train2.append(letters.index(result_str.lower()))
        #else:
        #    # convert from RGB to Unit RGB
        #    x_train.append(train)
        #    y_train.append(train2)
        #    train2=[]
        #    train=[]
        #    train.append(imageToMatrice.astype("float32") / 255)
        #    train2.append(letters.index(result_str.lower()))
        #    font = result_str2

        # reshape from (60000, 28, 28) into (60000, 784)
        #np.shape(
        #x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1] * x_train.shape[2]))
        #np.append(x_train, np.reshape(x_train, (np.shape(x_train)[0], np.shape(x_train)[1] * np.shape(x_train)[2])))
    
        # labels
    print(language["Import25"],end='')
    for i1 in range(len(x_train)):
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
    print(language["Import50"],end='')
    w = []
    z = []
    for i in range(len(inp)):
        w.append(np.reshape(inp[i].ravel(), (-1, 1)).astype(np.float32))
        z.append(np.reshape(goal_pred[i].ravel(), (-1, 1)).astype(np.float32))
    #inp = np.array(w)
    #goal_pred = np.array(z)
    print(language["Import75"],end='')
    numbers = np.arange(len(w))
    numbers = shuffle(numbers)
    #print(sort_by_indexes(w, numbers))
    inp = np.array(sort_by_indexes(w, numbers))
    goal_pred = np.array(sort_by_indexes(z, numbers))
    
    print(language["ImportDone"])
    return inp, goal_pred
