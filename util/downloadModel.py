import requests
import os
from tqdm import tqdm
import html
import gradio as gr
#import time

def getModels(url):#, logging):
    try:
        response = requests.get(url)
    except Exception as err:
        #logging.warning("E034",exc_info=True)
        return None
    #logging.info(response.status_code)
    if not response.status_code == 200:
        #logging.warning("E034")
        return None
    remoteModels = response.json()["models"]
    return remoteModels

def downloadModel(url, name, extension):#remoteModel):#, logging):
    #strq += '[' + Fore.GREEN + str(i) + Fore.RESET + ']' + remoteModels[i]["name"] +' ('+remoteModels[i]["date"]+')'+ '\n'
    print(url, name, extension)
    try:
        responseModel = requests.get(url, stream=True)
        total_size = int(responseModel.headers.get("content-length", 0))
        block_size = 1024
        #logging.debug(total_size)
    except Exception as err:
        #logging.warning("E034",exc_info=True)
        #print(Fore.RED + language['ErrorConnect'] + Fore.RESET)
        return
    if not responseModel.status_code == 200:
        #logging.warning("E034")
        #print(Fore.RED + language['ErrorConnect'] + Fore.RESET)
        return
    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', name+'.'+extension), "wb") as file:
            for data in responseModel.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
    #if total_size != 0 and progress_bar.n != total_size:
        #logging.error("Could not download file")
    #with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', remoteModels[remoteModelsNum]["fullname"]), 'wb') as f:
    #    f.write(responseModel.content)

def createTable(urlConfig):
    models = getModels(urlConfig)
    #<!-- {time.time()} -->
    codeTable = f"""
    <table id="modelsTable">
        <thead>
            <tr>
                <th>Название</th>
                <th>Дата</th>
                <th>Вес</th>
                <th>Скачать</th>
            </tr>
        </thead>
        <tbody>"""
    for model in models:
        name = model["name"]
        date = model["date"]
        url = model["url"]
        extension = model["extension"]
        size = model["size"]
        fullname = name+'.'+extension
        existing = False
        #x = "Hello"
        codeTable += f"""
            <tr>
                <td>{html.escape(name)}</td>
                <td>{html.escape(date)}</td>
                <td>{html.escape(size)}</td>
                <td><a href='{html.escape(url)}' download='{html.escape(fullname)}'><button class='lg secondary  svelte-cmf5ev'>Установить</button></a></td>
            </tr>"""
        codeTable += """
        </tbody>
    </table>"""
    return codeTable

def createTable0(urlConfig):
    models = getModels(urlConfig)
    codeTable = f"""
    <table>
        <thead>
            <tr>
                <th>Название</th>
                <th>Дата</th>
                <th>Вес</th>
                <th>Скачать</th>
            </tr>
        </thead>
    </table>
        """
    for model in models:
        name = model["name"]
        date = model["date"]
        url = model["url"]
        extension = model["extension"]
        size = model["size"]
        fullname = name+'.'+extension
        existing = False
        #x = "Hello"
        codeTable += f"""
        <table>
            <tr>
                <td>{html.escape(name)}</td>
                <td>{html.escape(date)}</td>
                <td>{html.escape(size)}</td>
            </tr>
        </table>"""
        codeTable += """
        </tbody>
    </table>"""
    return codeTable
#print(createTable("https://huggingface.co/Morkovka21Vek/AI_Font_Generator/raw/main/config.json"))
# <td><button onclick="downloadModel(this, '{html.escape(url)}', '{html.escape(name)}', '{html.escape(extension)}')" {"disabled=disabled" if existing else ""}>{"Установить" if not existing else "Установлено"}</button></td>