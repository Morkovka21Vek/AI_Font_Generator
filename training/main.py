try:
    import logging
    import os
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "main_log.log")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "main_log.log"))
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "main_log.log"),filemode="w",format="%(asctime)s %(levelname)s %(message)s")
except Exception as e:
    print("E003", e)
    input()
    quit()
try:
    import json
    import datetime
    import numpy as np
    from numba import jit, prange, vectorize, cuda
    from safetensors.numpy import save_file, load_file
    #from tqdm import tqdm#, tzip
except Exception as e:
    logging.error("E001",exc_info=True)
    print("E001")
    input()
    quit() 
logging.info("Import lib Done!") 
try:
    import utils
except Exception as e:
    logging.error("E025",exc_info=True)
    print("E025")
    input()
    quit()

@jit(nopython=True, fastmath=True, cache=True, parallel=True)
def sigmoid(num):
    return 1 / (1 + np.exp(-num))
    #return num

@jit(nopython=True, fastmath=True)#, cache=True)#, parallel=True)
def train(inp_const, goal_pred_const, hiddenLayerQuantity, weight, epochs, learning_rate, bias, w_hid_out, b_hid_out, w_inp_hid):
    for epoch in prange(epochs):
        #sys.stdout.write('\r Epoch:', epoch, round(epoch / epochs * 100, 2), '%')
        print('Epoch:', epoch, round(epoch / epochs * 100, 2), '%')
        #print(epoch)
        for inp, goal_pred in zip(inp_const, goal_pred_const):
            hidden = []
            hidden.append(sigmoid(bias[0] + np.dot(w_inp_hid, inp)))
            for i in prange(0, hiddenLayerQuantity-1):
                hidden.append(sigmoid(bias[i+1] + np.dot(weight[i], hidden[i-1])))
            pred = sigmoid(b_hid_out + np.dot(w_hid_out, hidden[-1]))#.astype(np.float32)
            #hidden = np.array(hidden)
            #e_loss += 1 / outLayer * np.sum((pred - goal_pred) ** 2, axis=0)
            delta_output = pred - goal_pred
            w_hid_out -= learning_rate * np.dot(delta_output, np.transpose(hidden[-1]))
            b_hid_out -= learning_rate * delta_output
            if hiddenLayerQuantity > 1:
                delta_hidden = np.dot(np.transpose(w_hid_out), delta_output) * (hidden[-1] * (1 - hidden[-1]))
                weight[-1] -= np.dot(delta_hidden, np.transpose(hidden[-2])) * learning_rate
                bias[-1] -= learning_rate * delta_hidden
                delta_hidden2 = delta_hidden
                if hiddenLayerQuantity > 2:
                    for i in prange(hiddenLayerQuantity - 2, 0, -1):
                        delta_hidden = np.dot(np.transpose(weight[-i]), delta_hidden2) * (hidden[-(1+i)] * (1 - hidden[-1+i]))
                        weight[-(1+i)] -= np.dot(delta_hidden, np.transpose(hidden[-(2+i)])) * learning_rate
                        bias[-(1+i)] -= learning_rate * delta_hidden
                        delta_hidden2 = delta_hidden

            delta_hidden = np.dot(np.transpose(weight[0]), delta_hidden2) * (hidden[0] * (1 - hidden[0]))
            w_inp_hid -= np.dot(delta_hidden, np.transpose(inp)) * learning_rate
            bias[0] -= learning_rate * delta_hidden
    return weight, bias, w_hid_out, b_hid_out, w_inp_hid

inpQ = input("Нажмите Enter если хотите обучить новую нейросеть, или перетащите сюда файл модели для продолжения обучения: >>>").replace('"', '').replace("'", '')
logging.debug(f"inp = {inpQ}")
#inp_const, goal_pred_const = utils.load_dataset()

inp_const = np.array([[[0], [1], [0], [0], [1], [0], [0], [1], [0]],
                [[1], [1], [0], [0], [1], [0], [1], [1], [1]],
                [[1], [1], [0], [0], [1], [1], [1], [1], [0]],
              ]).astype(np.float32)

goal_pred_const = np.array([[[0], [1], [0], [0], [1], [0], [0], [1], [0]],
                [[1], [1], [0], [0], [1], [0], [1], [1], [1]],
                [[1], [1], [0], [0], [1], [1], [1], [1], [0]],
              ]).astype(np.float32)
#inp_const = np.round(inp_const, 0)
#goal_pred_const = np.round(goal_pred_const, 0)
#print('Округление(доп. функция) завершено!')
#np.set_printoptions(threshold=np.inf)
#========================---------========================#
inpLayer = 9#1226#Xshape * Yshape + 1#1226
hiddenLayer = 20
outLayer = 9#1225
hiddenLayerQuantity = 2  # min 2
epochs = 100000
learning_rate = 0.001#0.001
Xshape = 35
Yshape = 35
#========================---------========================#

if inpQ == "":
    logging.info("Creating new")
    bias = []
    for i in prange(hiddenLayerQuantity):
        bias.append(np.zeros((hiddenLayer, 1), dtype=np.float32))
    b_hid_out = np.zeros((outLayer, 1), dtype=np.float32)
    bias = np.array(bias)
    
    weight = []
    w_inp_hid = np.random.rand(hiddenLayer, inpLayer).astype(np.float32)
    for i in prange(hiddenLayerQuantity-1):
        weight.append(np.random.rand(hiddenLayer, hiddenLayer).astype(np.float32))

    weight = np.array(weight)
    w_hid_out = np.random.rand(outLayer, hiddenLayer).astype(np.float32)
else:
    logging.info("loading model")
    weight=[]
    bias=[]
    weightData = load_file(inpQ)
    for i in range(weightData['weightLen']):
        weight.append(weightData[f'weight{i+1}'])
    w_hid_out = weightData['weights_hidden_to_output']
    w_inp_hid = weightData['weights_input_to_hidden']
    for i in range(weightData['biasLen']):
        bias.append(weightData[f'bias{i+1}'])
    b_hid_out = weightData['bias_hidden_to_output']
    hiddenLayer, inpLayer = w_inp_hid
    outLayer = w_hid_out[0]
    hiddenLayerQuantity = weightData['weightLen']+1
    
logging.info("Start training")
weight_out, bias_out, w_hid_out_out, b_hid_out_out, w_inp_hid_out = train(inp_const, goal_pred_const, hiddenLayerQuantity, weight, epochs, learning_rate, bias, w_hid_out, b_hid_out, w_inp_hid)
logging.info("End training")
hidden=[]
hidden.append(sigmoid(bias_out[0] + np.dot(w_inp_hid_out, inp_const[0])).astype(np.float32))
for i in prange(0, hiddenLayerQuantity-1):
    hidden.append(sigmoid(bias_out[i] + np.dot(weight_out[i], hidden[i-1])).astype(np.float32))
pred = sigmoid(b_hid_out_out + np.dot(w_hid_out_out, hidden[-1])).astype(np.float32)
for pr, goal_pr_c in pred, goal_pred_const[0]:
    print(pr, goal_pr_c)
curent_time = datetime.datetime.now()
directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
logging.info(f"Out Dir: {directory}")
saved_arrays = {}
for i, array in enumerate(weight_out):
    saved_arrays[f'weight{i+1}'] = array
for i, array in enumerate(bias_out):
    saved_arrays[f'bias{i+1}'] = array
saved_arrays['weights_hidden_to_output'] = w_hid_out_out
saved_arrays['bias_hidden_to_output'] = b_hid_out_out
saved_arrays['weightLen'] = len(weight)
saved_arrays['biasLen'] = len(bias)
saved_arrays['Xshape'] = Xshape
saved_arrays['Yshape'] = Yshape
saved_arrays['weights_input_to_hidden'] = w_inp_hid_out
saveNameStr = 'model{}X{}_{}layers{}neurons'.format(outLayer, Xshape, hiddenLayerQuantity, hiddenLayer)
if os.path.exists(os.path.join(directory, saveNameStr+'.safetensors')):
    index = 2
    while True:
        if os.path.exists(os.path.join(directory, saveNameStr+'({}).safetensors'.format(index))):
            index+=1
        else:
            save_file(saved_arrays, os.path.join(directory, saveNameStr+'({})'.format(index)+'.safetensors'))
            logging.info("save file:"+os.path.join(directory, saveNameStr+'({})'.format(index)+'.safetensors'))
            break
else:
    save_file(saved_arrays, os.path.join(directory, saveNameStr+'.safetensors'))
    logging.info("save file:"+os.path.join(directory, saveNameStr+'.safetensors'))

print("ModelSave")
logging.debug('Program End')
input()
#hidden=[]
#hidden.append(sigmoid(bias_out[0] + w_inp_hid_out @ inp_const[0]).astype(np.float32))
#for i in prange(0, hiddenLayerQuantity-1):
#    hidden.append(sigmoid(bias_out[i] + weight_out[i] @ hidden[i-1]).astype(np.float32))
#pred = sigmoid(b_hid_out_out + w_hid_out_out @ hidden[-1]).astype(np.float32)
#print(pred, goal_pred_const[0])