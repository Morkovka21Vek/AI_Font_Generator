import gradio as gr
#import numpy as np
import random
from util.model import createTable, downloadModel, getSaveModels, setInteractiveModelName, getNameFromUrl#, getModels
from util.settings import save_settings, import_settings
from util.generator import generate_font
from util.font2img import font2img, saveImages
import util.createFolders
import os
import logging

def init_loger(name):
    logger = logging.getLogger(name)
    FORMATE = "%(asctime)s - %(name)s: %(funcName)s: %(lineno)d - %(levelname)s - %(message)s"
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMATE))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_log.log"), mode="a")
    fh.setFormatter(logging.Formatter(FORMATE))
    fh.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.info("Start logging")
    

init_loger("app")
logger = logging.getLogger("app.app")

settings = import_settings()
logger.info(f"settings: {str(settings)}")

def checkLogLimit(limit):
    if limit == -1:
        return False
    size = os.path.getsize("app_log.log")/1048576
    if size > limit:
        return True
    return False

#<span style="color:blue">some *blue* text</span>
with gr.Blocks(title="AI Font Generator") as demo:
    with gr.Row():
        gr.Markdown('# <span style="color:orange">AI Font Generator</span> <span style="color:red">(альфа)</span>')
        gr.Markdown('## <span style="color:red">Лимит логов превышен!</span>', visible=checkLogLimit(settings["maxLogFileSize"]))
    with gr.Tab("Генерация"):
        with gr.Column():
            with gr.Row():
                with gr.Column():
                    File_Input_Svg = gr.File(file_count="multiple", file_types=(None if settings["IS_DEBUG"] else ["svg"]), label="svg")
                    with gr.Row():
                        Generate_Button = gr.Button("Генерировать", variant="primary")
                        download_Result_Button = gr.Button("📥", interactive=False, scale=0) #📥
                    #    image_input = gr.Image(file_count = "multiple")
            
                with gr.Column():
                    with gr.Group():
                        #gr.Markdown("## Настройки.")
                        with gr.Row():
                            selectSaveModel = gr.Dropdown(getSaveModels(settings), interactive=True, value=settings["DefaultSaveModel"], label="Выбор модели")
                            #selectSaveModel_Refresh_Button = gr.Button("\U0001f504", scale=0) #🔄
                        slider = gr.Slider(0, 1, label="Смещение", step=0.1)
                        with gr.Row():
                            seed_number = gr.Number(label="Сид", interactive=True, value=int(random.randrange(4294967294)))
                            random_seed_button = gr.Button("\U0001f3b2\ufe0f", scale=0) #🎲️
            
            generate_image_outputs = gr.Gallery(label="Выходные изображения")
                
    with gr.Tab("ШрифтВизобр"):
        with gr.Row():
            with gr.Column():
                File_Input_Font = gr.File(file_count="single", file_types=(None if settings["IS_DEBUG"] else ["ttf", "otf"]), label="otf, ttf")
                Generate_font2img_Button = gr.Button("Генерировать", variant="primary")
            with gr.Column():
                font2img_checkBox_mode = gr.Radio(["png", "svg"], label="Преобразовать в")
                Save_font2img_Button = gr.Button("Сохранить",interactive=False)
                Download_font2img_Button = gr.DownloadButton("Загрузить",interactive=True,visible=False)
                Save_Images_font2img_Type = gr.Radio(["png", "jpg"], label="Расширение сохраняемых картинок", value="png")
                Sent_font2img_To_Generate_Button = gr.Button("Отправить на генерацию", interactive=False)
        font2svg_image_outputs = gr.Gallery(label="Выходные изображения", format="png", columns=7)
    
    with gr.Tab("Настройки", visible=settings["Visible_Settings"]):
        Config_Url_textbox = gr.Textbox(label="Ссылка на конфиг по умолчанию", interactive=True, value=settings["Config_Url"])
        selectDefaultSaveModel = gr.Dropdown(getSaveModels(settings, True), interactive=True, value=settings["DefaultSaveModel"], label="Выбор модели по умолчанию")
        Is_Show_Extension_In_Models = gr.Checkbox(value=settings["Is_Show_Extension_In_Models"], interactive=True, label="Отображать расширение моделей")
        maxLogFileSize = gr.Number(settings["maxLogFileSize"], label="Максимальный размер файла логов в МБ (НЕ УДАЛЯЕТСЯ, ТОЛЬКО ОПОВЕЩЕНИЕ)(0 - отключить)", interactive=True, minimum=0, step=0.1)
        PngFontSize_Settings_slider = gr.Slider(1, 200, value=settings["PngFontSize"], step=1, label="Размер шрифта при экспорте в png во вкладке ШрифтВизобр")
        save_settings_button = gr.Button("Сохранить", variant="primary")
        
    with gr.Tab("Модели", visible=settings["Visible_Models_Download"]):
        with gr.Group():
            url_download_model = gr.Textbox(label="ссылка на модель", interactive=True)
            download_model_button = gr.Button("Скачать", variant="primary")
            with gr.Row():
                name_download_model = gr.Textbox(label="Название загружаемой модели", interactive=False)
                checkBox_name_download_model = gr.Checkbox(False, label="Вручную", scale=0)
        with gr.Group():
            with gr.Row():
                url_text_models = gr.Textbox(label="ссылка на конфиг", interactive=True, value=settings["Config_Url"])
                reset_url_button = gr.Button("сбросить", scale=0)
            download_config_button = gr.Button("Показать", variant="primary")
        models_table_html = gr.HTML()
        
    Debug_Tab = gr.Tab("Отладка", visible = settings["IS_DEBUG"])
    with Debug_Tab:
        get_var_list_button = gr.Button("Получить список переменных")
        var_list_Md = gr.Text("", interactive=False)

    Generate_Button.click(generate_font, inputs=File_Input_Svg, outputs=generate_image_outputs)
    random_seed_button.click(lambda: int(random.randrange(4294967294)), outputs=seed_number)
    save_settings_button.click(save_settings, inputs=[Config_Url_textbox, selectDefaultSaveModel, Is_Show_Extension_In_Models, maxLogFileSize, PngFontSize_Settings_slider])
    reset_url_button.click(lambda: settings["Config_Url"], outputs=url_text_models)
    download_config_button.click(lambda url: createTable(url, settings), inputs=url_text_models, outputs=models_table_html)
    Generate_font2img_Button.click(lambda *args: font2img(*args, settings), inputs=[File_Input_Font, font2img_checkBox_mode], outputs=[Save_font2img_Button, Download_font2img_Button, Sent_font2img_To_Generate_Button, font2svg_image_outputs])
    get_var_list_button.click(lambda: str(globals()), outputs=var_list_Md)
    download_model_button.click(downloadModel, inputs=[url_download_model, name_download_model])
    checkBox_name_download_model.input(setInteractiveModelName, inputs=[checkBox_name_download_model, name_download_model, url_download_model], outputs=name_download_model)
    url_download_model.input(getNameFromUrl, inputs=[checkBox_name_download_model, url_download_model], outputs=name_download_model)
    Save_font2img_Button.click(saveImages, inputs=[Save_Images_font2img_Type, font2img_checkBox_mode, File_Input_Font], outputs=[Save_font2img_Button, Download_font2img_Button])
    Save_Images_font2img_Type.input(lambda: [gr.Button("Сохранить",interactive=True, visible=True), gr.DownloadButton("Загрузить",interactive=True, visible=False)], outputs=[Save_font2img_Button, Download_font2img_Button])

if settings["IS_SHARE"]:
    demo.launch(share=True)
else:
    demo.launch()
