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
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "crop_log.log"), mode='w')

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

def xRF(img):
    xR = 0
    for x in range(img.size[0]):
        flag = False
        for y in range(img.size[1]):
            #print(im.getpixel((x, y)), f)
            if img.getpixel((x, y)) != 0:
                flag = True
        if flag == False and xR <= x:
            xR = x
        else:
            return xR

def yUF(img):
    yU = 0
    for y in range(img.size[1]):
        flag = False
        for x in range(img.size[0]):
            #print(im.getpixel((x, y)), f)
            if img.getpixel((x, y)) != 0:
                flag = True
        if flag == False and yU <= y:
            yU = y
        else:
            return yU

def xLF(img):
    xL = img.size[0]
    for x in range(img.size[0]-1, -1, -1):
        flag = False
        for y in range(img.size[1]):
            #print(im.getpixel((x, y)), f)
            if img.getpixel((x, y)) != 0:
                flag = True
        if flag == False and xL >= x:
            xL = x
        else:
            return xL
        
def yDF(img):
    yD = img.size[1]
    for y in range(img.size[1]-1, -1, -1):
        flag = False
        for x in range(img.size[0]):
            #print(im.getpixel((x, y)), f)
            if img.getpixel((x, y)) != 0:
                flag = True
        if flag == False and yD >= y:
            yD = y
        else:
            return yD


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
            xR=xRF(im)
        except Exception as err:
            logger.error("E016(xRF)",exc_info=True)
            input()
            quit()
        try:
            yU=yUF(im)
        except Exception as err:
            logger.error("E016(yUF)",exc_info=True)
            input()
            quit()
        try:
            xL=xLF(im)
        except Exception as err:
            logger.error("E016(xLF)",exc_info=True)
            input()
            quit()
        try:
            yD=yDF(im)
        except Exception as err:
            logger.error("E016(yDF)",exc_info=True)
            input()
            quit()
        im = im.crop((xR, yU, xL, yD))
        logger.debug((xR, yU, xL, yD))
        try:
            im.save(filename)
        except Exception as err:
            logger.error("E017",exc_info=True)
    print(language["program_End"])
    logger.debug('Program End')
    input()
except Exception as err:
    logger.error('E000',exc_info=True)
    input()