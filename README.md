# <u>**AI_Font_Generator**</u><small>(Beta)</small> ![Static Badge](https://img.shields.io/badge/Version-0.5.0-green)  

<p align="center">
  <a href="https://github.com/Morkovka21Vek/AI_Font_Generator/releases"><img src="https://img.shields.io/github/downloads/Morkovka21Vek/AI_Font_Generator/total.svg?style=flat&logo=github" alt="Github All Releases"/></a>
  <a href="https://github.com/Morkovka21Vek/AI_Font_Generator/releases"><img src="https://img.shields.io/github/release/Morkovka21Vek/AI_Font_Generator.svg?style=flat&logo=github" alt="GitHub release"/></a>
</p>
<p align="center">
  <a href="https://huggingface.co/Morkovka21Vek/AI_Font_Generator"><img src="https://img.shields.io/badge/Huggingface-models-yellow" alt="huggingface models"/></a>
</p>

## [RU]Создает остальные символы шрифта на основе имеющихся с помощью ИИ.  
<p align="center">
  <a href="https://colab.research.google.com/drive/15sg7_-Ipu91oK3Up_qZPF1puczsIIjYK#scrollTo=k8IBtFYxe6Jo"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Демо версия."/></a>
</p>

 [![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/+PZdpMF19QdU0NTUy)

 >ПРИ ЗАПУСКЕ В ПЕРВЫЙ РАЗ ЗАПУСТИТЕ СКРИПТ ```settings.py```! 

 Установка если есть git⬇️:
 ```Shell
 git clone https://github.com/Morkovka21Vek/AI_Font_Generator.git
 ```

 Установка библиотек:
 ```Shell
 pip install -r requirements.txt
 ``` 
 

<details>
<summary><h3>Как ипользовать?</h3></summary> 

### ОБУЧЕНИЕ(tarining):  
1. В папку ```input``` поместите шрифты(рекомендуется не менее 5 штук)  
2. Запустите ```ttf2png.py``` 
3. Запустите ```main.py```  
4. Переместить модель из папки ```training\output``` в ```usage\models```  
### ИСПОЛЬЗОВАНИЕ(usage):  
1. Запустите ```ttf2png.py``` и передайте ему путь к шрифту(или перетащите файл в окно консоли)  
2. Запустите ```main.py```  

</details> 

<details>
<summary><h3>Коды ошибок:</h3></summary>  

- E000 - Неизвестная ошибка.
- E001 - Ошибка импорта библиотек.
- E002 - Ошибка импорта файла с настройками (```settings.json```) (попробуйте запустить ```settings.py```).
- E003 - Ошибка настройки логов.(NOLOG)
- E004 - ~~Ошибка импорта ```FontForge```.~~
- E005 - Ошибка Выбора файла и загрузки шрифта, а также выгрузки всех символов из него(может не поддерживаться шрифт).
- E006(W) - Ошибка измерения размера изображения, создания изображения и отрисовки на нём текста.
- E007 - ~~Ошибка экспорта.~~
- E009 - Ошибка открытия изображения.
- E010 - Ошибка просмотра пикселей на изображении.
- E011 - Ошибка удаления изображения.
- E012 - Ошибка подготовки строки с выбором модели/шрифта.
- E013 - Ошибка преобразования строки в число.
- E014(W014) - Ошибка ввода номера которого нет в списке.
- E016 - Ошибка выполнения функции поиска крайних пикселей (```xRF, xLF, yUf, yDF```)
- E017 - Ошибка сохранения файла.
- E018 - Ошибка изменения размера изображения.
- E019 - Ошибка ввода чисел.
- E020 - Ошибка преобразования изображения в ```numpy array```.
- E021 - Ошибка преобразования листа в ```numpy array```.
- E022 - Ошибка импорта модели.
- E023 - Ошибка выгрузки переменных из модели.
- E025 - Ошибка импорта скрипта ```utils```.
- E027 - Ошибка вычисления выхода нейросети.
- E028 - Ошибка преобразования ```numpy array``` в изображение.
- E029 - Ошибка настройки папки для шрифта.
- E034(W) - Ошибка подключения к интернету.

</details>


## [EN]Creates the remaining symbols of the font based on the available AI.  
     
 >WHEN STARTING FOR THE FIRST TIME RUN THE SCRIPT ```settings.py```!  
 
 Installation if there is git⬇️:
 ```Shell
 git clone https://github.com/Morkovka21Vek/AI_Font_Generator.git
 ```
 
 Install libraries:
 ```Shell
 pip install -r requirements.txt
 ``` 

<details>
<summary><h3>How to use?</h3></summary> 

### TRAINING:
1. Place fonts in the ```input``` folder (at least 5 are recommended)  
2. Run ```ttf2png.py```
3. Run ```main.py```  
4. Move the model from the ```training\output``` folder to ```usage\models```  
### USAGE:  
1. Run ```ttf2png.py``` and give it the full path to the font (or drag the file into the console window)  
2. Run ```main.py```  

</details> 

<details>
<summary><h3>Error codes:</h3></summary>  

- E000 is an unknown mistake.
- E001 - Library import error.
- E002 - File importing error (```settings.json```) (try to run ```settings.Py```).
- E003 - error setting up logs. (NOLOG)
- E004 - ~~import error ```fontforge```.~~
- E005 - a file selection error and font loading, as well as unloading all characters from it (the font may not be maintained).
- E006 (W) - error of measuring the size of the image, creating an image and drawing on it of the text.
- E007 - ~~Export error.~~
- E009 - an error of opening the image.
- E010 - A mistake to view pixels in the image.
- E011 - an error of removal of the image.
- E012 - error of preparing a line with the choice of model/font.
- E013 - error of converting the line into the number.
- E014 (W014) - an entry error of which is not on the list.
- E016 - error in performing the function of searching for extreme pixels (`` `XRF, XLF, Yuf, ydf```
- E017 - File saving error.
- E018 - error of changing the size of the image.
- E019 - Error input of numbers.
- E020 - an error of converting the image in ```numpy array``` '.
- E021 - A mistake of converting a sheet into ```numpy Array``` '.
- E022 - Model import error.
- E023 - error of unloading variables from the model.
- E025 - a script import error ```utils```.
- E027 - error in calculating the output of the neural network.
- E028 - Transforming error ```numpy array``` in the image.
- E029 - error setting up the font folder.
- E034 (W) - error of Internet connection.
</details>       