try:
    import os
    import json
    #import traceback
    import sys
    import logging
    import shutil
except Exception as e:
    print("E001", e)
    input()
    quit()

try:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logger.addHandler(console_handler)
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "ttf2png_log.log"), mode='w')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
except Exception as e:
    print("E003", e)
    input()
    quit()    

try:
    import fontforge
except Exception as err:
    #logger.info("Новый импорт FontForge")
    if not os.path.basename(sys.executable) == "ffpython.exe":
        os.system(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "other", "ffpython", "bin", "ffpython.exe")+' '+__file__)
        quit()
    else:
        logger.error('E004')
        input()
        quit()

logger.info("Import libraries Done!")
#"C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" ttf2png.py
try:
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
            language = json.load(f)["Language"]
        logger.info("Import language Done")
    except Exception as err:
        logger.error('E002',exc_info=True)
        input()
        quit()
    try:
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input')
        if not os.path.exists(directory):
            os.makedirs(directory)
        directoryOut = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_png')
        if not os.path.exists(directoryOut):
            os.makedirs(directoryOut)
    except Exception as err:
        logger.error('E006',exc_info=True)
        input()
        quit()
    try:
        files = os.listdir(directory)
    except Exception as err:
        logger.error('E015',exc_info=True)
        input()
        quit()
    try:
        strq=''
        for i in range(len(files)):
            strq += '[' + str(i) + ']' + files[i] + '\n'
        print(strq)
    except Exception as err:
        logger.error('E012',exc_info=True)
        input()
        quit()
    try:
        startNum=int(input(language["Start_s"]))
        endNum=int(input(language["End"]))
    except Exception as err:
        logger.error('E013',exc_info=True)
        input()
        quit()
    if not (startNum >= 0 and endNum >= 0 and endNum < len(files)):
        logger.error('E014')
        input()
        quit()
    try:
        for i in range(startNum, endNum+1):
            fileinputname = os.path.join(directory, files[i])# + '.ttf'
            F = fontforge.open(fileinputname)
            for name in F:
                filename = os.path.join(directoryOut, str(i) + "." + name + ".png")
                F[name].export(filename)
        logger.info(language["Export {} end({})"]. format(fileinputname, i))
    except Exception as err:
        logger.error('E007',exc_info=True)
        input()
        quit()
    print(language["program_End"])
    logger.debug('Program End')
    input()
except Exception as err:
    logger.error('E000',exc_info=True)
    input()
