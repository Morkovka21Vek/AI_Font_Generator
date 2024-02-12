import numpy as np
#import matplotlib.image
import os
import utils
from PIL import Image
from tqdm import tqdm
import json
import traceback


#Xshape = 35

#def tanh(num):
#    return (np.exp(num) - np.exp(-num)) / (np.exp(num) + np.exp(-num))

def sigmoid(num):
    return 1 / (1 + np.exp(-num))
    #return num


def Start(inp_const, weight, Xshape, directoryOut, bias, weights_hidden_to_output, bias_hidden_to_output, Yshape, weights_input_to_hidden):
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for stLetter in tqdm(range(len(inp_const))):
        for letter in range(len(letters)):
            #inp = np.reshape(inp_const[stLetter], (-1, 1))
            #layers=[]
            #layers.append(np.dot(np.append(inp, letter), weight[0]))
            #print(len(weight))
            #print(letter, letters[letter])
            #for i in range(1, len(weight)-1):
            #    #layers.append(np.dot(layers[i-1], weight[i]))
            #    npd = np.dot(layers[i-1], weight[i])
            #    for x in range(len(npd)):
            #        #npd[x] = npd[x]/10000000#10**7
            #        npd[x] = truncate(npd[x], 5)
            #    layers.append(npd)
                    
            #npd = np.dot(layers[len(weight)-2], weight[len(weight)-1])
            #for x in range(len(npd)):
            #    npd[x] = truncate(npd[x], 5)
            #layers.append(npd)
            #pred = np.dot(layers[len(layers)-1], weight[len(weight)-1]).reshape((Xshape, int(np.shape(weight[len(weight)-1])[1]/Xshape)))
            #pred = np.dot(layers[len(layers)-1], weight[len(weight)-1])
            #for y in range(len(pred)):
            #    for x in range(len(pred[y])):
            #        pred[y][x] = tanh(pred[y][x])
            #        if pred[y][x] < 0:
            #            pred[y][x] = 0
            #print(pred)
            #pred = (pred - pred.min())/(pred.max() - pred.min()).reshape((Xshape, int(np.shape(weight[len(weight)-1])[1]/Xshape)))
            hidden=[]
            inp = np.reshape(np.append(inp_const[stLetter], letter/(len(letters)-1)), (-1, 1))
            #hidden.append(sigmoid(bias[0] + np.dot(weight[0], np.append(inp_const[0], letter/len(letters)-1))))
            hidden.append(sigmoid(bias[0] + np.dot(weights_input_to_hidden, inp)))
            for i in range(len(weight)):
                hidden.append(sigmoid(bias[i+1] + np.dot(weight[i], hidden[i-1])))
            pred = sigmoid(bias_hidden_to_output + np.dot(weights_hidden_to_output, hidden[-1]))
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
            pred = pred.reshape((Xshape, Yshape))
            im = Image.fromarray(pred*255)
            im = im.convert('RGB')
            #matplotlib.image.imsave(directoryOut + '\\' + letters[i] + '.png', pred)
            im.save(directoryOut + '\\' + str(stLetter) + '.' + letters[letter] + '.png', format='PNG')

with open(os.path.abspath(os.getcwd())+'\\settings.json', encoding='utf-8') as f:
    language = json.load(f)["Language"]
    
try:
#if True:
    directory = os.path.realpath('out_png')
    directoryModel = os.path.realpath('models')
    directoryOut = os.path.realpath('out_main')
    files = os.listdir(directory)
    filesModel = os.listdir(directoryModel)
    strq=language["SelectFont"]
    for i in range(len(files)):
        strq += '[' + str(i) + ']' + files[i] + '\n'
    strq += '>>>'
    num = int(input(strq))
    strq=language["SelectModel"]
    for i in range(len(filesModel)):
        if not '_bias' in filesModel[i]:
            strq += '[' + str(i) + ']' + filesModel[i] + '\n'
    strq += '>>>'
    numModel = int(input(strq))
    directory = directory + '\\' + files[num]
    directoryModel = directoryModel + '\\' + filesModel[numModel]
    print(directory, directoryModel)
    files = os.listdir(directory)
    inp, weight, bias, weights_hidden_to_output, bias_hidden_to_output, Xshape, Yshape, weights_input_to_hidden = utils.load_dataset(directory, files, directoryModel)
    #print(type(weight[1]))
    Start(inp, weight, Xshape, directoryOut, bias, weights_hidden_to_output, bias_hidden_to_output, Yshape, weights_input_to_hidden)
    print(language["Programm_End"])
    input()
except IndexError:
    print(language["ErrorNumber"])
    input()
except Exception:
    print(language["Exception"])
    traceback.print_exc()
    input()
