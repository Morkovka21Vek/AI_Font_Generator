import os
import json
import gradio as gr

def save_settings(Config_Url_textbox, selectDefaultSaveModel):
    standard_settings = import_settings()
    Settings = {
        "Config_Url": Config_Url_textbox,
        "DefaultSaveModel": selectDefaultSaveModel,
        "IS_DEBUG": standard_settings["IS_DEBUG"],
        "Visible_Settings": standard_settings["Visible_Settings"],
        "Visible_Models_Download": standard_settings["Visible_Models_Download"],
        "IS_SHARE": standard_settings["IS_SHARE"]
        }
    file = json.dumps(Settings, ensure_ascii=False, indent=4)
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'settings.json'), 'w', encoding='utf-8') as f:
        f.write(file)
    gr.Info("Данные сохранены!")
    
def import_settings():
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'settings.json'), encoding='utf-8') as f:
        settings = json.load(f)
    return settings