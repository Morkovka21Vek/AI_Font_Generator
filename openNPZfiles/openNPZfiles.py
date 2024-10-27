import numpy as np
import os
from matplotlib import pyplot as plt
from colorama import Fore, init
init()

while True:
    # path = "C:\\Users\\User\\Desktop\\LEFTYCAS.npz"
    path = input("Путь к .npz файлу: >>> ").replace('"', '').replace("'", "")
    if path == '':
        break

    # print([value for value in np.load(path).values()])
    npzFile = np.load(path)
    values = [value for value in npzFile.values()]
    keys = [value for value in npzFile.keys()]

    printStr = ""

    for i, key in enumerate(keys):
        printStr += f"[{Fore.GREEN}{i}{Fore.RESET}] {Fore.YELLOW}{key}{Fore.RESET} {chr(int(key))}\n"

    while True:
        svgPath = '<?xml version="1.0" encoding="utf-8" ?>\n<svg baseProfile="full" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="50 -20 100 100" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n<defs />\n<path d="'
        inp = input(printStr+">>> ")
        if inp == '':
            break
        
        try:
            inp = int(inp)
        except:
            print(f"{Fore.RED}Неудалось преобразовать в int{Fore.RESET}")
            continue

        if inp >= 0 and inp < len(values):
            print(values[inp].shape)
            # plt.plot(values[inp][:, 0], values[inp][:, 1], "bo")    
            plt.plot(values[inp][:, 0], values[inp][:, 1]*-1+1)
            for i, pos in enumerate(values[inp]):
                plt.text(pos[0], pos[1]*-1+1, str(i), color="r", fontsize="x-small")
                if i <= 0:
                    svgPath += f"M {pos[0]*100}, {pos[1]*100}"
                elif i%2 == 1:
                    svgPath += f" Q {values[inp][i-1][0]*100} {values[inp][i-1][1]*100} {pos[0]*100} {pos[1]*100}"
            svgPath += ' S " stroke="#000000" stroke-width="2" />\n</svg>'
            with open("C:\\Users\\User\\Desktop\\outNpzLetter.svg", mode="w") as file:
                file.write(svgPath)
            plt.show()
        else:
            print(f"{Fore.RED}Неверное число{Fore.RESET}")
            continue

