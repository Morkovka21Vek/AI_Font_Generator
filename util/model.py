import requests
import os
from tqdm import tqdm
import html
import gradio as gr
#import time

def getSaveModels(settings, flag=False):
    x = os.listdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models'))
    if not settings["Is_Show_Extension_In_Models"]:
        for i, n in enumerate(x):
            x[i] = os.path.splitext(n)[0]
    if flag:
        x.append(None)
        return x
    return x

def getModels(url: str):#, logging):
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

def downloadModel(url: str, model_Name: str):#, name, extension):#remoteModel):#, logging):
    #strq += '[' + Fore.GREEN + str(i) + Fore.RESET + ']' + remoteModels[i]["name"] +' ('+remoteModels[i]["date"]+')'+ '\n'
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
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', model_Name), "wb") as file:
            for data in responseModel.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
    gr.Info(f"Модель {model_Name} успешно установлена!")
    #return getSaveModels()
    #if total_size != 0 and progress_bar.n != total_size:
        #logging.error("Could not download file")
    #with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', remoteModels[remoteModelsNum]["fullname"]), 'wb') as f:
    #    f.write(responseModel.content)

def createTable(urlConfig: str, settings):
    models = getModels(urlConfig)
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
        return model_Name

#print(createTable("https://huggingface.co/Morkovka21Vek/AI_Font_Generator/raw/main/config.json"))
# <td><button onclick="downloadModel(this, '{html.escape(url)}', '{html.escape(name)}', '{html.escape(extension)}')" {"disabled=disabled" if existing else ""}>{"Установить" if not existing else "Установлено"}</button></td>