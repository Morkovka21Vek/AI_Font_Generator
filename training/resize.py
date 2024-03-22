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
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "resize_log.log"), mode='w')
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

def resize_images(input_path, output_path, new_size=(40, 40)):
    try:
        img = Image.open(input_path)
    except Exception as err:
        logger.error("E009",exc_info=True)
        input()
        quit()
    try:
        resized_img = img.resize(new_size)
    except Exception as err:
        logger.error("E018",exc_info=True)
        input()
        quit()
    try:
        resized_img.save(output_path)
    except Exception as err:
        logger.error("E017",exc_info=True)
        input()
        quit()

try:
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
            language = json.load(f)["Language"]
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
    try:
        xyInp = input(language["SizeImgXY"]).split(' ')
        x = int(xyInp[0])
        y = int(xyInp[1])
    except Exception as err:
        logger.error('E019',exc_info=True)
        input()
        quit()
    for f in files:
        filename = os.path.join(directory, f)
        resize_images(filename, filename, (x,y))
    print(language["program_End"])
    logger.debug('Program End')
    input()
except Exception as err:
    logger.error('E000',exc_info=True)
    input()
