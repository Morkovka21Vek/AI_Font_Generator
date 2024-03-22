try:
    import os
    import json
    import logging
    import datetime
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
    from numba import jit, prange
except Exception as e:
    print("E032", e)
    input()
    quit()
#try:
#    from tqdm import tqdm
#except Exception as e:
#    print("E026", e)
#    input()
#    quit()
    
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

@jit(nopython=True, fastmath=True, cache=True)
def sigmoid(num):
    return 1 / (1 + np.exp(-num))
    #return num

@jit(nopython=True, fastmath=True, cache=True)#, parallel=True)
#@vectorize(['int32(int32, int32)', 'int64(int64, int64)', 'float32(float32, float32)', 'float64(float64, float64)'])
#@vectorize
def train(inp_const, goal_pred_const, hiddenLayerQuantity, weight, epochs, learning_rate, bias, weights_hidden_to_output, bias_hidden_to_output, weights_input_to_hidden):
    for epoch in prange(epochs):
        #e_loss = 0
        #e_correct = 0
        #loss = []
        #accuracy = []
        #print('Epoch: ', epoch, ' ', round(epoch / epochs * 100, 1), '%', sep='')
        print(epoch)
        for number in prange(len(inp_const)):
            inp = inp_const[number]
            #inp = np.reshape(inp_const[number], (-1, 1))
            #goal_pred = np.reshape(goal_pred_const[number], (-1, 1))
            #print(inp)
            goal_pred = goal_pred_const[number]

            hidden = []#np.array([])
            hidden.append(sigmoid(bias[0] + np.dot(weights_input_to_hidden, inp)))
            for i in prange(0, hiddenLayerQuantity-1):
                hidden.append(sigmoid(bias[i+1] + np.dot(weight[i], hidden[i-1])))
            pred = sigmoid(bias_hidden_to_output + np.dot(weights_hidden_to_output, hidden[-1]))#.astype(np.float32)#.astype(np.float64)
            hidden = np.array(hidden)
            #print(pred)

            #e_loss += 1 / outLayer * np.sum((pred - goal_pred) ** 2, axis=0)
            #e_loss += (pred - goal_pred)#1 / outLayer * np.sum((pred - goal_pred), axis=0)
            #e_correct += int(np.argmax(pred) == np.argmax(goal_pred))
            #print(pred)


            delta_output = pred - goal_pred
            weights_hidden_to_output += -learning_rate * np.dot(delta_output, np.transpose(hidden[-1]))
            bias_hidden_to_output += -learning_rate * delta_output
            
            delta_hidden2 = delta_output
            delta_hidden = np.transpose(weights_hidden_to_output) @ delta_hidden2 * (hidden[-1] * (1 - hidden[-1]))
    		#weights[-1] += -learning_rate * delta_hidden @ np.transpose(image)
            #print(type(delta_hidden[0][0]), type(np.transpose(hidden[-2][0][0])), type(hidden[-2][0][0]))
            #weight[-1] += -learning_rate * delta_hidden @ np.transpose(hidden[-2])
            weight[-1] += delta_hidden @ np.transpose(hidden[-2]) * -learning_rate
            bias[-1] += -learning_rate * delta_hidden
            delta_hidden2 = delta_hidden

            if True:
                for i in range(hiddenLayerQuantity - 2, 0, -1):
                    delta_hidden = np.transpose(weight[-i]) @ delta_hidden2 * (hidden[-(1+i)] * (1 - hidden[-1+i]))
            		#weights[-1] += -learning_rate * delta_hidden @ np.transpose(image)
                    #np.array([learning_rate]).astype(np.float32)[0]
                    weight[-(1+i)] += delta_hidden @ np.transpose(hidden[-(2+i)]) * -learning_rate
                    bias[-(1+i)] += -learning_rate * delta_hidden
                    delta_hidden2 = delta_hidden

            delta_hidden = np.transpose(weight[0]) @ delta_hidden2 * (hidden[0] * (1 - hidden[0]))
            weights_input_to_hidden += delta_hidden @ np.transpose(inp) * -learning_rate
            #weights[-1] += -learning_rate * delta_hidden @ np.transpose(hidden[-2])
            bias[0] += -learning_rate * delta_hidden
                
            
            #print(bias)

        #loss.append(round((e_loss[0] / len(inp_const) / inpLayer) * 100, 3))
        #accuracy.append(round((e_correct / len(inp_const) / inpLayer) * 100, 3))
        #print(f"Loss: {round((e_loss[0] / inpLayer) * 100, 3)}%")
        #print(f"Accuracy: {round((e_correct / inpLayer) * 100, 3)}%")
    return weight, bias, weights_hidden_to_output, bias_hidden_to_output, weights_input_to_hidden

inp_const, goal_pred_const = utils.load_dataset()

#inp_const = np.array([[[0], [1], [0], [0], [1], [0], [0], [1], [0]],
#                 [[1], [1], [0], [0], [1], [0], [1], [1], [1]],
#                 [[1], [1], [0], [0], [1], [1], [1], [1], [0]],
#               ]).astype(np.float32)

#goal_pred_const = np.array([[[0], [1], [0], [0], [1], [0], [0], [1], [0]],
#                 [[1], [1], [0], [0], [1], [0], [1], [1], [1]],
#                 [[1], [1], [0], [0], [1], [1], [1], [1], [0]],
#               ]).astype(np.float32)
#inp_const = np.round(inp_const, 0)
#goal_pred_const = np.round(goal_pred_const, 0)
#print('Округление(доп. функция) завершено!')
#np.set_printoptions(threshold=np.inf)
#========================НАСТРОЙКИ========================#
inpLayer = 1226#Xshape * Yshape + 1#1226
hiddenLayer = 2
outLayer = 1225
hiddenLayerQuantity = 2  # min 2 ТОЛЬКО 2
epochs = 10000
learning_rate = 0.001#0.001
Xshape = 35
Yshape = 35
#========================НАСТРОЙКИ========================#
    
bias = []
for i in prange(hiddenLayerQuantity):
    bias.append(np.zeros((hiddenLayer, 1), dtype=np.float32))
#bias.append(np.zeros((outLayer, 1), dtype=np.float64))
bias_hidden_to_output = np.zeros((outLayer, 1), dtype=np.float32)
bias = np.array(bias)
  
weight = []#np.array([])
#weight.append(np.ones((hiddenLayer, inpLayer), dtype=np.float64))
#for i in prange(hiddenLayerQuantity-1):
#    weight.append(np.ones((hiddenLayer, hiddenLayer), dtype=np.float64))
#weights_hidden_to_output = np.ones((outLayer, hiddenLayer), dtype=np.float64)
weights_input_to_hidden = np.random.rand(hiddenLayer, inpLayer).astype(np.float32)
#weight.append(np.random.rand(hiddenLayer, inpLayer).astype(np.float32))
for i in prange(hiddenLayerQuantity-1):
    #np.append(weight, np.random.rand(hiddenLayer, hiddenLayer).astype(np.float32), axis=0)
    weight.append(np.random.rand(hiddenLayer, hiddenLayer).astype(np.float32))

weight = np.array(weight)
weights_hidden_to_output = np.random.rand(outLayer, hiddenLayer).astype(np.float32)
#weight = np.array(weight)
#print('Перехожу дальше с epochs = {}, alpha = {}, inpLayer = {}, hiddenLayer = {}, outLayer = {}, hiddenLayerQuantity = {}, а длина inp_const = {}'.format(epochs,
#                                                                                        alpha,inpLayer,hiddenLayer,outLayer,hiddenLayerQuantity,len(inp_const)))
#print(bias[0])
logger.info("Start training")
weight_out, bias_out, weights_hidden_to_output_out, bias_hidden_to_output_out, weights_input_to_hidden_out = train(inp_const, goal_pred_const, hiddenLayerQuantity, weight, epochs, learning_rate, bias, weights_hidden_to_output, bias_hidden_to_output, weights_input_to_hidden)
logger.info("End training")
#print(f"Loss: {round((e_loss[0] / inpLayer) * 100, 3)}%")
#print(f"Accuracy: {round((e_correct / inpLayer) * 100, 3)}%")
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
    language = json.load(f)["Language"]
curent_time = datetime.datetime.now()
#print(f"100.0%\nНейросеть закончила обучение {curent_time}. Дождитесь окончания сохранения модели.")
directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
#saved_arrays = {}
#for i, array in enumerate(weight_out):
#    saved_arrays[f'array{i+1}'] = array
    
#np.savez(directory+'model{}X{}_{}layers{}neurons{}-{}-{}'.format(outLayer, Xshape, hiddenLayerQuantity, hiddenLayer,
#                                                        curent_time.day, curent_time.month, curent_time.year),  **saved_arrays)
saved_arrays = {}
#saved_arrays_bias = {}
for i, array in enumerate(weight_out):
    saved_arrays[f'weight{i+1}'] = array
for i, array in enumerate(bias_out):
    #saved_arrays_bias[f'bias{i+1}'] = array
    saved_arrays[f'bias{i+1}'] = array
saved_arrays['weights_hidden_to_output'] = weights_hidden_to_output_out
#saved_arrays_bias['bias_hidden_to_output'] = bias_hidden_to_output_out
saved_arrays['bias_hidden_to_output'] = bias_hidden_to_output_out
saved_arrays['weightLen'] = len(weight)
saved_arrays['biasLen'] = len(bias)
saved_arrays['Xshape'] = Xshape
saved_arrays['Yshape'] = Yshape
saved_arrays['weights_input_to_hidden'] = weights_input_to_hidden_out
if os.path.exists(os.path.join(directory, 'model{}X{}_{}layers{}neurons{}-{}-{}.npz'.format(outLayer, Xshape, hiddenLayerQuantity, hiddenLayer,curent_time.day, curent_time.month, curent_time.year))):
    index = 2
    #print('OK1')
    while True:
        if os.path.exists(os.path.join(directory, 'model{}X{}_{}layers{}neurons{}-{}-{}({}).npz'.format(outLayer, Xshape, hiddenLayerQuantity, hiddenLayer,curent_time.day, curent_time.month, curent_time.year, index))):
            index+=1
        else:
            np.savez(os.path.join(directory, 'model{}X{}_{}layers{}neurons{}-{}-{}({})'.format(outLayer, Xshape, hiddenLayerQuantity, hiddenLayer,
                                                        curent_time.day, curent_time.month, curent_time.year, index)),  **saved_arrays)
            break
else:
    np.savez(os.path.join(directory, 'model{}X{}_{}layers{}neurons{}-{}-{}'.format(outLayer, Xshape, hiddenLayerQuantity, hiddenLayer,
                                                        curent_time.day, curent_time.month, curent_time.year)),  **saved_arrays)
#np.savez(directory+'model{}X{}_{}layers{}neurons{}-{}-{}'.format(outLayer, Xshape, hiddenLayerQuantity, hiddenLayer,
#                                                        curent_time.day, curent_time.month, curent_time.year),  **saved_arrays)
#np.savez(directory+'model{}X{}_{}layers{}neurons{}-{}-{}_bias'.format(outLayer, Xshape, hiddenLayerQuantity, hiddenLayer,
#                                                        curent_time.day, curent_time.month, curent_time.year),  **saved_arrays_bias)

print(language["ModelSave"])
logger.debug('Program End')
input()
#hidden=[]
#hidden.append(sigmoid(bias_out[0] + weights_input_to_hidden_out @ inp_const[0]).astype(np.float32))
#for i in prange(0, hiddenLayerQuantity-1):
#    hidden.append(sigmoid(bias_out[i] + weight_out[i] @ hidden[i-1]).astype(np.float32))
#pred = sigmoid(bias_hidden_to_output_out + weights_hidden_to_output_out @ hidden[-1]).astype(np.float32)
#print(pred, goal_pred_const[0])