import os
import numpy as np
from PIL import Image

def load_dataset(directory, files, directoryModel):
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    inp=[]
    Xshape = 0
    font=0
    weight=[]
    bias=[]
    for file in files:
        img = Image.open(directory + '\\' + file)
        imageToMatrice = np.asarray(img)
        #print(imageToMatrice.shape)
        inp.append(imageToMatrice.ravel())
    inp_np = np.array(inp)
    #weight = np.load(directoryModel)
    weightData = np.load(directoryModel)
    for i in range(weightData['weightLen']):
        weight.append(weightData[f'weight{i+1}'])
    weights_hidden_to_output = weightData['weights_hidden_to_output']

    for i in range(weightData['biasLen']):
        bias.append(weightData[f'bias{i+1}'])
    bias_hidden_to_output = weightData['bias_hidden_to_output']

    Xshape = weightData['Xshape']
    Yshape = weightData['Yshape']
    
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
    print('Импорт успешно завершён!')
    return inp_np, weight, bias, weights_hidden_to_output, bias_hidden_to_output, Xshape, Yshape
