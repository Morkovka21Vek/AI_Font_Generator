try:
    from PIL import Image
except Exception as e:
    print("E008", e)
    input()
    quit()
try:
    import os
    import json
    import logging
except Exception as e:
    print("E001", e)
    input()
    quit()

try:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "del_log.log"), mode='w')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
except Exception as e:
    print("E003", e)
    input()
    quit()

logger.debug("Import Done!")

try: 
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
            language = json.load(f)["Language"]
        logger.debug("Import language Done")
    except Exception as err:
        logger.error('E002',exc_info=True)
        input()
        quit()
    try:
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_png')
        files = os.listdir(directory)
        logger.debug("Open folder Done")
    except Exception as err:
        logger.error('E006',exc_info=True)
        input()
        quit()
    for f in files:
        try:
            filename = os.path.join(directory, f)
            im = Image.open(filename)
        except Exception as err:
            logger.error("E009",exc_info=True)
            input()
            quit()
        try:
            flag = False
            for x in range(im.size[0]):
                for y in range(im.size[1]):
                    if im.getpixel((x, y)) != 0:
                        flag = True
        except Exception as err:
            logger.error("E010",exc_info=True)
            input()
            quit()
        try:
            if flag == False:
                os.remove(filename)
                logger.info('delete file: ', filename)
        except Exception as err:
            logger.error("E011",exc_info=True)
            input()
            quit()
    print(language["program_End"])
    logger.debug('Program End')
    input()
except Exception as err:
    logger.error('E000',exc_info=True)
    input()
