import numpy as np
import os
import keras
from matplotlib import pyplot as plt

folderDatasetsArrPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trainingDatasetArray")
listDatasetsArr = os.listdir(folderDatasetsArrPath)
fullListDatasetsArr = [os.path.join(folderDatasetsArrPath, i) for i in listDatasetsArr]
datasetArr = []
#my_dic = {key: value for key, value in results['scores'].items()}
#my_dic = [value for key, value in results['scores'].items()]
for path in fullListDatasetsArr:
    datasetArr.extend([value.ravel() for key, value in np.load(path).items()])
    # datasetArr.append(np.load(path))
# print(datasetArr)
# datasetArrList =  [font.values() for font in datasetArr]
# datasetArrList =  [i[1] for char in datasetArr for i in char.items()]
datasetArrTest = datasetArr[0].reshape((200, 2))
datasetArrX = [i[0] for i in datasetArrTest]
datasetArrY = [i[1] for i in datasetArrTest]
# print(datasetArr[0].reshape((200, 2)))
# plt.plot(datasetArr[0].reshape((200, 2)), "bo")
# plt.plot(datasetArrX, datasetArrY, "bo")
# plt.show()

print(np.shape(datasetArr))
datasetArr = np.array(datasetArr)
# print(datasetArr)

#tensorboard --logdir C:\Users\User\Documents\GitHub\AI_Font_Generator\training\logs
tensorboard = keras.callbacks.TensorBoard(log_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"), write_graph=True)

model = keras.Sequential([
        #   keras.layers.Input()
          keras.layers.Dense(1000, input_shape=(400,)),
          keras.layers.Activation('relu'),
          keras.layers.Dense(700, input_shape=(1000,)),
          keras.layers.Activation('relu'),
          keras.layers.Dense(400, input_shape=(700,)),
          keras.layers.Activation('relu')
        ])
model.compile(loss='categorical_crossentropy',
              optimizer='adam')#,
            #   #metrics=['accuracy'])

history = model.fit(datasetArr, datasetArr,
                    # batch_size=batch_size,
                    epochs=5000,
                    verbose=1,
                    validation_split=0.1,
                    callbacks=[tensorboard])
plt.plot(history.history["loss"])
plt.grid(True)
plt.show()

# print(datasetArr[0].shape)
plt.plot(datasetArrX, datasetArrY, "bo")
# model.predict(datasetArr[0].reshape((1, 400))).reshape((200, 2))
datasetArrTestCreate = model.predict(datasetArr[0].reshape((1, 400))).reshape((200, 2))
datasetArrXCreate = [i[0] for i in datasetArrTestCreate]
datasetArrYCreate = [i[1] for i in datasetArrTestCreate]
plt.plot(datasetArrXCreate, datasetArrYCreate, "ro")
plt.show()
