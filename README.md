# AI_Font_Generator(Beta version) version: 0.3.3  
 [EN]Creates the rest of the font characters using AI.(translated by Yandex translator)  
 I have a thc with news on the project https://t.me /+PZdpMF19QdU0NTUy (only in Russian)  
 TO WORK, YOU NEED TO INSTALL FontForge(https://fontforge.org/en-US/downloads/windows /) REMEMBER THE PATH TO THE PROGRAM  

     
 TRAINING:  
    0.At startup, run the script for the first time creatFolders.py  
    1.Place fonts in the "input" folder (at least 5 are recommended)  
    2.Run start_ttf2png.bat (if it does not start, go to the folder with the FontForge program next\bin\ffpython.exe click on it with PCM+SHIFT and select "Copy as path", then click on start_ttf2png.bat and click "Edit" then replace "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" on the way to ffpython.exe )  
    3.Run del.py  
    4.Run crop.py  
    5.Launch resize.py  
    6.Run main.py_new  
    7.Move the model from the training/output folder to usage/models  
 USAGE:  
    0.When running for 1 time, run the script creatFolders.py  
    1.Run start_ttf2png.bat (if it does not start, go to the folder with the FontForge program next \bin\ffpython.exe click on it with PCM+SHIFT and select "Copy as path", then click on start_ttf2png.bat and click "Edit" then replace "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" to the ffpython path.exe) and give it the full path to the font (or drag the file into the console window)(ATTENTION! If the names of the 2 match, the new font will change the old one, which may lead to an error)  
    2.Run del.py  
    3.Run crop.py  
    4.Run resize.py  
    5.Run main.py  
    6.Run gray2rgb.py (none)  
    7.Run png2svg.py  
    8.Run svg2ttf.py (none)  
       
 [RU]Создает остальные символы шрифта с помощью ИИ.  
 У меня есть тгк с новостями по проекту https://t.me/+PZdpMF19QdU0NTUy  
 ДЛЯ РАБОТЫ НУЖНО УСТАНОВИТЬ FontForge(https://fontforge.org/en-US/downloads/windows/) ЗАПОМНИТЕ ПУТЬ К ПРОГРАММЕ  
 ОБУЧЕНИЕ(tarining):  
    0.При запуске впервые запустите скрипт creatFolders.py  
    1.В папку "input" поместите шрифты(рекомендуется не менее 5 штук)  
    2.Запустите start_ttf2png.bat(если не запускается перейдите в папку с программой FontForge далее \bin\ffpython.exe кликните по ней ПКМ+SHIFT и выберите "Копировать как путь" далее кликните ПКМ по start_ttf2png.bat и нажмите "Изменить" далее замените "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" на путь к ffpython.exe)  
    3.Запустите del.py  
    4.Запустите crop.py  
    5.Запустите resize.py  
    6.Запустите main.py  
    7.Переместить модель из папки training/output в usage/models  
 ИСПОЛЬЗОВАНИЕ(usage):  
    0.При запуске в 1 раз запустите скрипт creatFolders.py  
    1.Запустите start_ttf2png.bat(если не запускается перейдите в папку с программой FontForge далее \bin\ffpython.exe кликните по ней ПКМ+SHIFT и выберите "Копировать как путь" далее кликните ПКМ по start_ttf2png.bat и нажмите "Изменить" далее замените "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" на путь к ffpython.exe) и передайте ему полный путь к шрифту(или перетащите файл в окно консоли)(ВНИМАНИЕ! Если названия 2-х будут совпадать то новый шрифт изменит старый, что может привести к ошибке)  
    2.Запустите del.py  
    3.Запустите crop.py  
    4.Запустите resize.py  
    5.Запустите main.py  
    6.Запустите gray2rgb.py(нету)  
    7.Запустите png2svg.py  
    8.Запустите svg2ttf.py(нету)  
    
