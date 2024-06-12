import gradio as gr
#import numpy as np
import random
from util.downloadModel import createTable#, getModels, downloadModel
from util.settings import save_settings, import_settings
from util.generator import generate_font
from util.font2svg import font2svg
import os

settings = import_settings()

def getSaveModels(flag=False):
    x = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models'))
    if flag:
        x.append(None)
        return x
    return x


#<span style="color:blue">some *blue* text</span>
with gr.Blocks() as demo:
    #gr.Markdown('# <span style="color:orange">**AI_Font_Generator**</span>')
    gr.Markdown('# <span style="color:orange">AI Font Generator</span> <span style="color:red">(альфа)</span>')
    with gr.Tab("Главное"):
        with gr.Column():
            with gr.Row():
                with gr.Column():
                    #with gr.Tab("Шрифт"):
                    #gr.Markdown("## **В разработке!**")
                    File_Input_Svg = gr.File(file_count="multiple", file_types=["svg"], label="svg")
                    Generate_Button = gr.Button("Генерировать", variant="primary")

                    #with gr.Tab("Изображение"):
                    #    image_input = gr.Image(file_count = "multiple")
                    #    image_button = gr.Button("Сгенерировать", variant="primary")
            
                with gr.Column():
                    with gr.Group():
                        #gr.Markdown("## Настройки.")
                        selectSaveModel = gr.Dropdown(getSaveModels(), interactive=True, value=settings["DefaultSaveModel"], label="Выбор модели")
                        slider = gr.Slider(0, 1, label="Смещение", step=0.1)
                        with gr.Row():
                            seed_number = gr.Number(label="Сид", interactive=True, value=int(random.randrange(4294967294)))
                            random_seed_button = gr.Button("🎲️", scale=0)
                        #slider2 = gr.Slider(0,50)
            
            image_output = gr.Image()
    with gr.Tab("ШрифтВsvg"):
        with gr.Row():
            with gr.Column():
                File_Input_Font = gr.File(file_count="single", file_types=["ttf", "otf"], label="otf, ttf")
                Generate_Svg_Button = gr.Button("Генерировать", variant="primary")
            with gr.Column():
                Save_Svg_Button = gr.Button("Сохранить",interactive=False)
                Sent_Svg_To_Generate_Button = gr.Button("Отправить на генерацию", interactive=False)
    
    with gr.Tab("Настройки", visible=settings["Visible_Settings"]):
        Config_Url_textbox = gr.Textbox(label="Ссылка на конфиг по умолчанию", interactive=True, value=settings["Config_Url"])
        selectDefaultSaveModel = gr.Dropdown(getSaveModels(True), interactive=True, value=settings["DefaultSaveModel"], label="Выбор модели по умолчанию")
        #IS_DEBUG_BUTTON = gr.Checkbox(settings["IS_DEBUG"], label = "Отладка", interactive=True)
        save_settings_button = gr.Button("Сохранить", variant="primary")
        
    with gr.Tab("Модели", visible=settings["Visible_Models_Download"]):
        with gr.Row():
            url_text_models = gr.Textbox(label="ссылка", interactive=True, value=settings["Config_Url"])
            reset_url_button = gr.Button("сбросить", scale=0)
        download_config_button = gr.Button("Показать", variant="primary")
        #models_data_frame = gr.Dataframe(headers=["Название", ""], interactive=False)
        models_table_html = gr.HTML()
        #models_drop_down = gr.Dropdown()
        
    Debug_Tab = gr.Tab("Отладка", visible = settings["IS_DEBUG"])
    with Debug_Tab:
        gr.Markdown("## **В разработке!**")

    Generate_Button.click(generate_font, inputs=File_Input_Svg, outputs=image_output)
    random_seed_button.click(lambda: int(random.randrange(4294967294)), outputs=seed_number)
    save_settings_button.click(save_settings, inputs=[Config_Url_textbox, selectDefaultSaveModel])
    reset_url_button.click(lambda: settings["Config_Url"], outputs=url_text_models)
    download_config_button.click(createTable, inputs=url_text_models, outputs=models_table_html)
    Generate_Svg_Button.click(font2svg, inputs=File_Input_Font, outputs=[Save_Svg_Button, Sent_Svg_To_Generate_Button])

#demo = gr.Interface(fn=image_classifier, inputs="image", outputs="label")
demo.launch()#share=True)