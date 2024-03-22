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
    #file_handler = logging.FileHandler('log\\ttf2png_log.log')
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "ttf2png_log.log"), mode='w')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    #logging.basicConfig(level=logging.INFO, filename="log\\ttf2png_log.log",filemode="w",
    #                    format="%(asctime)s %(levelname)s %(message)s")
except Exception as e:
    print("E003", e)
    input()
    quit()
try:
    import fontforge
except Exception as err:
    #logger.info("Новый импорт FontForge")
    if not os.path.basename(sys.executable) == "ffpython.exe":
        #try:
        #    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
        #        settings = json.load(f)["Settings"]
        #except Exception as err:
        #    logger.error('E002',exc_info=True)
        #    input()
        #    quit()
        os.system(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "other", "ffpython", "bin", "ffpython.exe")+' '+__file__)
        #print("OK")
        #os.system('cd '+settings["directoryToAI_Font_Generator"]+'\\usage')
        quit()
    else:
        logger.error('E004')
        input()
        #logger.info("Exit")
        quit()

logger.info("Import libraries Done!")

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
        fileinputname = input(language["InputFilePath"]).replace('"', '').replace("'", '')
        logger.info(f"Entrance file name: {fileinputname}")
        F = fontforge.open(fileinputname)
    except Exception as err:
        logger.error('E005',exc_info=True)
        input()
        quit()
    logger.info("Import font Done")
    try:
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_png')#os.path.realpath('out_png')
        if not os.path.exists(filename):
            os.makedirs(filename)
    except Exception as err:
        logger.error('E006',exc_info=True)
        input()
        quit()
    try:
        if not os.path.exists(os.path.join(filename, os.path.splitext(os.path.basename(fileinputname))[0])):
            filename = os.path.join(filename, os.path.splitext(os.path.basename(fileinputname))[0])
            os.makedirs(filename)
        else:
            inp = os.path.splitext(os.path.basename(fileinputname))[0]
            while True:
                print(language["SelectNameForFontWithName"].format(inp))
                inp = input(">>> ")
                if inp == "Yes" or inp == "Да":
                    filename = os.path.join(filename, os.path.splitext(os.path.basename(fileinputname))[0])
                    shutil.rmtree(filename)
                    os.makedirs(filename)
                    break
                elif not inp == '':
                    if not os.path.exists(os.path.join(filename, inp)):
                        filename = os.path.join(filename, inp)
                        os.makedirs(filename)
                        break
    except Exception as err:
            logger.error("E011",exc_info=True)
            input()
            quit()
    
    logger.debug("Open folder Done")
        
    try:
        for name in F:
            #print(filename + '\\' + name + '.png')
            F[name].export(os.path.join(filename, name+'.png'))
    except Exception as err:
        logger.error('E007',exc_info=True)
        input()
        quit()
    #logger.info(language["program_End"])
    print(language["program_End"])
    logger.debug('program End')
    input()
except Exception as err:
    logger.error('E000',exc_info=True)
    #traceback.print_exc()
    input()
