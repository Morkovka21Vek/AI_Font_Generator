try:
    import logging
    import os
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "ttf2png_log.log"),filemode="w",format="%(asctime)s %(levelname)s %(message)s")
except Exception as e:
    print("E003", e)
    input()
    quit()
try:
    import json
    from PIL import Image, ImageFont, ImageDraw
    from fontTools.ttLib import TTFont
    import shutil
    from tqdm import tqdm
    from colorama import Fore
except Exception as e:
    logging.error("E001",exc_info=True)
    print("E001")
    input()
    quit()

def xRF(img):
    xR = 0
    for x in range(img.size[0]):
        flag = False
        for y in range(img.size[1]):
            #print(im.getpixel((x, y)), f)
            #print(img.getpixel((0, 0)))
            if img.getpixel((x, y)) != (0,0,0,0):
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
            if img.getpixel((x, y)) != (0,0,0,0):
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
            if img.getpixel((x, y)) != (0,0,0,0):
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
            if img.getpixel((x, y)) != (0,0,0,0):
                flag = True
        if flag == False and yD >= y:
            yD = y
        else:
            return yD

try:
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), encoding='utf-8') as f:
            jsonFile = json.load(f)
            language = jsonFile["Language"]
            settings = jsonFile["Settings"]
        logging.info("Import language Done")
    except Exception as err:
        logging.error('E002',exc_info=True)
        print(Fore.RED+"E002"+Fore.RESET)
        input()
        quit()
    try:
        print(language["InputFilePath"], end='')
        fileinputname = input('>>>').replace('"', '').replace("'", '')
        logging.info(f"Entrance file name: {fileinputname}")
        font_size = 50
        logging.debug("Font_size: "+str(font_size))
        font = ImageFont.truetype(fileinputname, font_size)
        font_obg = TTFont(fileinputname)
        m_dict = font_obg.getBestCmap()
        desired_characters = []
        for key, _ in m_dict.items():
            desired_characters.append(key)
    except Exception as err:
        logging.error('E005',exc_info=True)
        print(Fore.RED+language["Exception"].format("E005")+Fore.RESET)
        input()
        quit()
    logging.info("Import font Done")
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_png')#os.path.realpath('out_png')
    logging.debug("Out_png dir: "+filename)
    if not os.path.exists(filename):
        os.makedirs(filename)
    try:
        if not os.path.exists(os.path.join(filename, os.path.splitext(os.path.basename(fileinputname))[0])):
            filename = os.path.join(filename, os.path.splitext(os.path.basename(fileinputname))[0])
            logging.info("Creating folder: "+filename)
            os.makedirs(filename)
        else:
            inp = os.path.splitext(os.path.basename(fileinputname))[0]
            logging.info("Start File Name: "+inp)
            while True:
                print(language["SelectNameForFontWithName"].format(Fore.YELLOW+inp+Fore.RESET))
                inp = input(">>>")
                logging.debug("Input: "+inp)
                if inp.lower() == "yes" or inp.lower() == "да":
                    filename = os.path.join(filename, os.path.splitext(os.path.basename(fileinputname))[0])
                    logging.info("Del directory: "+filename)
                    shutil.rmtree(filename)
                    os.makedirs(filename)
                    logging.info("Create directory: "+filename)
                    break
                elif not inp == '':
                    if not os.path.exists(os.path.join(filename, inp)):
                        filename = os.path.join(filename, inp)
                        logging.info("Creating directory: "+filename)
                        os.makedirs(filename)
                        break
    except Exception as err:
            logging.error("E011",exc_info=True)
            print(Fore.RED+language["Exception"].format("E011")+Fore.RESET)
            input()
            quit()
        
    try:
        for character in tqdm(desired_characters):
            try:
                left, top, right, bottom = font.getbbox(chr(character))
                width = right - left
                height = bottom - top
                img = Image.new("RGBA", (width, height))
                draw = ImageDraw.Draw(img)
                draw.text((0, -top), chr(character), font=font, fill="#000000")
            except Exception as err:
                logging.warning("E006", exc_info=True)
            try:
                xR=xRF(img)
                yU=yUF(img)
                xL=xLF(img)
                yD=yDF(img)
            except Exception as err:
                logging.error("E016",exc_info=True)
                print(Fore.RED+language["Exception"].format("E016")+Fore.RESET)
                input()
                quit()
            if xR != None and xL != None and yU != None and yD != None and xR < xL and yU < yD:
                img = img.crop((xR, yU, xL, yD))
                try:
                    img = img.resize(settings["modelPixelsImg"])
                except Exception as err:
                    logging.error("E018",exc_info=True)
                    print(Fore.RED+language["Exception"].format("E018")+Fore.RESET)
                    input()
                    quit()
                try:
                    img.save(os.path.join(filename, str(character) + ".png"))
                except:
                    logging.warning(f"notSave{character}({chr(character)})")
            else:
                logging.debug(f"empty {character}({chr(character)})")
    except Exception as err:
        logging.error('E007',exc_info=True)
        print(Fore.RED+language["Exception"].format("E007")+Fore.RESET)
        input()
        quit()
    #logging.info(language["program_End"])
    print(Fore.GREEN+language["program_End"]+Fore.RESET)
    logging.debug('program End')
    input()
except Exception as err:
    logging.error('E000',exc_info=True)
    print(Fore.RED+language["Exception"].format("E000")+Fore.RESET)
    input()
