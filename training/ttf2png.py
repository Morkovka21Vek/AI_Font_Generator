try:
    import logging
    import os
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"logs")):
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "ttf2png_log.log"),filemode="w",format="%(asctime)s %(levelname)s %(message)s")
except Exception as e:
    print("E003", e)
    input()
    quit()
directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input')
if not os.path.exists(directory):
    os.makedirs(directory)
    quit()

try:
    import json
    from PIL import Image, ImageFont, ImageDraw
    from fontTools.ttLib import TTFont
    from tqdm import tqdm
except Exception as e:
    logging.error("E001",exc_info=True)
    print("E001")
    input()
    quit()

logging.info("Import libraries Done!")

def xRF(img):
    xR = 0
    for x in range(img.size[0]):
        flag = False
        for y in range(img.size[1]):
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
        print("E002")
        input()
        quit()
    directoryOut = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_png')
    logging.debug("Out_png dir: "+directoryOut)
    if not os.path.exists(directoryOut):
        os.makedirs(directoryOut)
    files = os.listdir(directory)
    try:
        strq=''
        for i in range(len(files)):
            strq += '[' + str(i) + ']' + files[i] + '\n'
        print(strq)
    except Exception as err:
        logging.error('E012',exc_info=True)
        print("E012")
        input()
        quit()
    try:
        startNum=int(input(language["Start_s"]+' >>>'))
        endNum=int(input(language["End"]+' >>>'))
        logging.debug("StartNum: "+startNum+"; EndNum: "+endNum)
    except Exception as err:
        logging.error('E013',exc_info=True)
        print("E013")
        input()
        quit()
    if not (startNum >= 0 and endNum >= 0 and endNum < len(files)):
        logging.error('E014')
        print("E014")
        input()
        quit()
    try:
        font_size = 50
        logging.debug("Font_size: "+str(font_size))
        for i in range(startNum, endNum+1):
            fileinputname = os.path.join(directory, files[i])# + '.ttf'
            try:
                logging.info(f"Entrance file name: {fileinputname}")
                font = ImageFont.truetype(fileinputname, font_size)
                font_obg = TTFont(fileinputname)
                m_dict = font_obg.getBestCmap()
                desired_characters = []
                for key, _ in m_dict.items():
                    desired_characters.append(key)
            except Exception as err:
                logging.error('E005',exc_info=True)
                print("E005")
                input()
                quit()
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
                    print("E016")
                    input()
                    quit()
                if xR != None and xL != None and yU != None and yD != None and xR < xL and yU < yD:
                    img = img.crop((xR, yU, xL, yD))
                    try:
                        img = img.resize(settings["modelPixelsImg"])
                    except Exception as err:
                        logging.error("E018",exc_info=True)
                        print("E018")
                        input()
                        quit()
                    try:
                        filename = os.path.join(directoryOut, str(i) + "." + str(character) + ".png")
                        img.save(filename)
                    except:
                        logging.warning(f"notSave{character}({chr(character)})")
                else:
                    logging.debug(f"empty {character}({chr(character)})")
            logging.info("Export {} end({})".format(fileinputname, i))
    except Exception as err:
        logging.error('E007',exc_info=True)
        print("E007")
        input()
        quit()
    print(language["program_End"])
    logging.debug('Program End')
    input()
except Exception as err:
    logging.error('E000',exc_info=True)
    print("E000")
    input()
