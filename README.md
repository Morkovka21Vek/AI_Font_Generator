# <u>AI_Font_Generator</u><small>(Beta)</small> ![Static Badge](https://img.shields.io/badge/Version-0.4.0-green)  
![Static Badge](https://img.shields.io/badge/NoRelease-red)
## [EN]Creates the remaining symbols of the font based on the available AI.(translated by Yandex translator) 
     
 >WHEN STARTING FOR THE FIRST TIME RUN THE SCRIPT ```settings.py```!  
 
 Install libraries:
 ```Shell
 pip install -r requirements.txt
 ``` 

<details>
<summary><h3>How to use?</h3></summary> 

### TRAINING:
1. Place fonts in the ```input``` folder (at least 5 are recommended)  
2. Run ```ttf2png.py```
3. Run ```del.py```  
4. Run ```crop.py```  
5. Launch ```resize.py```  
6. Run ```main.py```  
7. Move the model from the ```training\output``` folder to ```usage\models```  
### USAGE:  
1. Run ```ttf2png.py``` and give it the full path to the font (or drag the file into the console window)  
2. Run ```del.py```  
3. Run ```crop.py```  
4. Run ```resize.py```  
5. Run ```main.py```  
6. Run ```png2svg.py``` (none)  
7. Run ```svg2ttf.py``` (none)  

</details> 

<details>
<summary><h3>Error codes:</h3></summary>  

- E000 - Unknown error.
- E001 - Built -in libraries import error.(NOLOG)
- E002 - File import error with settings (```settings.json```) (Try to start ```settings.py```).
- E003 - Error setting logs.(NOLOG)
- E004 - Import error ```FontForge```.
- E005 - An error of selecting a file and font loading (a font may not be maintained).
- E006 - The error in finding the path of folders in the system.
- E007 - Export error.
- E008 - Import error ```PIL```.(NOLOG)
- E009 - An image opening error.
- E010 - Error viewing pixels in the image.
- E011 - An image removal error.
- E012 - Error in preparing a line with the choice of model/font.
- E013 - The error of converting the line into the number.
- E014(W014) - The entry error of which is not on the list.
- E015 - Error search for all files in the folder.
- E016 - Error performing the function of searching for extreme pixels (```xRF, xLF, yUf, yDF```)
- E017 - File saving error.
- E018 - An error in the size of the image.
- E019 - Error input of numbers.
- E020 - An image conversion error into an ```numpy array```.
- E021 - The error of sheet converting into ```numpy array```.
- E022 - Model import error.
- E023 - Error unloading of variables from the model.
- E024 - Import error ```numpy```(NOLOG).
- E025 - The script import error ```utils```(NOLOG).
- E026 - Import error ```tqdm```(NOLOG).
- E027 - An error in calculating the output of the neural network.
- E028 - The transformation error ```numpy array``` in the image.
- E029 - Font folder setup error.
- E030 - ~~Import error ```colorama```(NOLOG).~~
- E031 - ~~Import error ```easygui```(NOLOG).~~
- E032 - Import error ```numba```

</details>       

## [RU]Создает остальные символы шрифта на основе имеющихся с помощью ИИ.  
 [![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/+PZdpMF19QdU0NTUy)

 >ПРИ ЗАПУСКЕ В ПЕРВЫЙ РАЗ ЗАПУСТИТЕ СКРИПТ ```settings.py```! 

 Установка библиотек:
 ```Shell
 pip install -r requirements.txt
 ``` 

<details>
<summary><h3>Как ипользовать?</h3></summary> 

### ОБУЧЕНИЕ(tarining):  
1. В папку ```input``` поместите шрифты(рекомендуется не менее 5 штук)  
2. Запустите ```ttf2png.py``` 
3. Запустите ```del.py```  
4. Запустите ```crop.py```  
5. Запустите ```resize.py```  
6. Запустите ```main.py```  
7. Переместить модель из папки ```training\output``` в ```usage\models```  
### ИСПОЛЬЗОВАНИЕ(usage):  
1. Запустите ```ttf2png.py``` и передайте ему полный путь к шрифту(или перетащите файл в окно консоли)  
2. Запустите ```del.py```  
3. Запустите ```crop.py```  
4. Запустите ```resize.py```  
5. Запустите ```main.py```  
6. Запустите ```png2svg.py``` (нету)  
7. Запустите ```svg2ttf.py``` (нету) 

</details> 

<details>
<summary><h3>Коды ошибок:</h3></summary>  

- E000 - Неизвестная ошибка.
- E001 - Ошибка импорта встроенных библиотек.(NOLOG)
- E002 - Ошибка импорта файла с настройками (```settings.json```) (попробуйте запустить ```settings.py```).
- E003 - Ошибка настройки логов.(NOLOG)
- E004 - Ошибка импорта ```FontForge```.
- E005 - Ошибка Выбора файла и загрузки шрифта(может не поддерживаться шрифт).
- E006 - Ошибка нахождения пути папок в системе.
- E007 - Ошибка экспорта.
- E008 - Ошибка импорта ```PIL```.(NOLOG)
- E009 - Ошибка открытия изображения.
- E010 - Ошибка просмотра пикселей на изображении.
- E011 - Ошибка удаления изображения.
- E012 - Ошибка подготовки строки с выбором модели/шрифта.
- E013 - Ошибка преобразования строки в число.
- E014(W014) - Ошибка ввода номера которого нет в списке.
- E015 - Ошибка поиска всех файлов в папке.
- E016 - Ошибка выполнения функции поиска крайних пикселей (```xRF, xLF, yUf, yDF```)
- E017 - Ошибка сохранения файла.
- E018 - Ошибка изменения размера изображения.
- E019 - Ошибка ввода чисел.
- E020 - Ошибка преобразования изображения в ```numpy array```.
- E021 - Ошибка преобразования листа в ```numpy array```.
- E022 - Ошибка импорта модели.
- E023 - Ошибка выгрузки переменных из модели.
- E024 - Ошибка импорта ```numpy```(NOLOG).
- E025 - Ошибка импорта скрипта ```utils```(NOLOG).
- E026 - Ошибка импорта ```tqdm```(NOLOG).
- E027 - Ошибка вычисления выхода нейросети.
- E028 - Ошибка преобразования ```numpy array``` в изображение.
- E029 - Ошибка настройки папки для шрифта.
- E030 - ~~Ошибка импорта ```colorama```(NOLOG).~~
- E031 - ~~Ошибка импорта ```easygui```(NOLOG).~~
- E032 - Ошибка импорта ```numba```

</details>