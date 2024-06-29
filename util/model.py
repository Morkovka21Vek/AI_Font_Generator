import requests
import os
from tqdm import tqdm
import html
import gradio as gr
import logging
logger = logging.getLogger("app.util.model")
#import time

def getSaveModels(settings, flag=False):
    x = os.listdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models'))
    logger.debug(f"saveModels list = {x}")
    if not settings["Is_Show_Extension_In_Models"]:
        for i, n in enumerate(x):
            x[i] = os.path.splitext(n)[0]
        logger.debug(f"saveModels no Extension list = {x}")
    if flag:
        x.append(None)
        return x
    return x

def getModels(url: str):#, logging):
    logger.info(f"getModels url: {url}")
    try:
        response = requests.get(url)
    except:
        logger.warning("No connection")
        gr.Warning("Ошибка подключения")
        return None
    #logging.info(response.status_code)
    if not response.status_code == 200:
        #logging.warning("E034")
        return None
    remoteModels = response.json()["models"]
    logger.debug(f"remoteModels list = {remoteModels}")
    return remoteModels

def downloadModel(url: str, model_Name: str):#, name, extension):#remoteModel):
    logger.info(f"downloadModel url: {url}, model_Name: {model_Name}")
    #strq += '[' + Fore.GREEN + str(i) + Fore.RESET + ']' + remoteModels[i]["name"] +' ('+remoteModels[i]["date"]+')'+ '\n'
    try:
        responseModel = requests.get(url, stream=True)
        total_size = int(responseModel.headers.get("content-length", 0))
        block_size = 1024
        logging.debug(f"total_size model = {total_size}")
    except:
        logger.warning("No connection")
        gr.Warning("Ошибка подключения")
        return
    if not responseModel.status_code == 200:
        logger.warning(f"responseModel.status_code = {responseModel.status_code}")
        gr.Warning("Ошибка подключения")
        return
    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', model_Name), "wb") as file:
            for data in responseModel.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
    gr.Info(f"Модель {model_Name} успешно установлена!")
    logger.info(f"Model {model_Name} has been successfully installed!")

def createTable(urlConfig: str, settings):
    logger.info(f"createTable urlConfig: {urlConfig}")
    models = getModels(urlConfig)
    if models is None:
        return None
    codeTable = f"""
    <table id="modelsTable">
        <thead>
            <tr>
                <th>Название</th>
                <th>Дата</th>
                <th>Вес</th>
                <th>Ссылка</th>
                <th>Ссылка текст</th>
            </tr>
        </thead>
        <tbody>"""
    for model in models:
        url = model["url"]
        name = getNameFromUrl(False, url)
        if not settings["Is_Show_Extension_In_Models"]:
            name = os.path.splitext(name)[0]
        date = model["date"]
        size = model["size"]
        #x = "Hello"
        codeTable += f"""
            <tr>
                <td>{html.escape(name)}</td>
                <td>{html.escape(date)}</td>
                <td>{html.escape(size)}</td>
                <td><a href='{html.escape(url)}'>ссылка</a></td>
                <td>{html.escape(url)}</td>
            </tr>"""
        codeTable += """
        </tbody>
    </table>"""
    return codeTable

def setInteractiveModelName(flag, name, url):
    if flag:
        return gr.Textbox(name, label="Название загружаемой модели", interactive=True)
    else:
        model_Name = getNameFromUrl(False, url)
        return gr.Textbox(model_Name, label="Название загружаемой модели", interactive=False)

def getNameFromUrl(flag, url):
    if not flag:
        model_Name = url.split('/')[-1]
        logger.debug(f"Model name from url = {model_Name}")
        return model_Name

#print(createTable("https://huggingface.co/Morkovka21Vek/AI_Font_Generator/raw/main/config.json"))
# <td><button onclick="downloadModel(this, '{html.escape(url)}', '{html.escape(name)}', '{html.escape(extension)}')" {"disabled=disabled" if existing else ""}>{"Установить" if not existing else "Установлено"}</button></td>