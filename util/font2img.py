import gradio as gr
from fontTools.ttLib import TTFont
from freetype import Face, FT_Curve_Tag, FT_Curve_Tag_On, FT_Vector
from PIL import Image, ImageFont, ImageDraw
import os
import io
import zipfile
import shutil
import logging
import sys
from tempfile import TemporaryFile, TemporaryDirectory
from util.TtfSvgConverter import TtfSvgConverter

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# https://github.com/mathandy/svgpathtools
from libs.svgpathtools import (wsvg, Line, CubicBezier, QuadraticBezier, Path)

logger = logging.getLogger("app.util.font2img")

convertImages = []

def font2img(pathToFont: str, mode: str, settings):
    global convertImages
    logger.info(f"pathToFont = {pathToFont}, mode = {mode}")
    if mode is None:
        gr.Warning("Выберите тип")
        return (gr.Button("Сохранить",interactive=True),gr.DownloadButton("Загрузить", visible=False),gr.Button("Отправить на генерацию", interactive=False),[])
    if pathToFont is None:
        gr.Warning("Выберите шрифт")
        return (gr.Button("Сохранить",interactive=True),gr.DownloadButton("Загрузить", visible=False),gr.Button("Отправить на генерацию", interactive=False),[])
    font_obg = TTFont(pathToFont)
    m_dict = font_obg.getBestCmap()
    zipFilePath = TemporaryFile(suffix='.zip')# suffix='.zip'
    # print(zipfile)
    if mode == "svg":
        # shutil.rmtree(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache'))
        # os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache', 'svgFont2img'))
        temp_dir = TemporaryDirectory()
        print(temp_dir.name, zipFilePath.name+'.zip')
        converter = TtfSvgConverter(ttfPath=pathToFont)
        for key, text in m_dict.items():
            converter.generate(text, os.path.join(temp_dir.name, str(key)+".svg"), mode=0)
        shutil.make_archive(zipFilePath.name, 'zip', temp_dir.name)
        gr.Info("Преобразование завершено!")
        logger.info("Done!")
        return (
            gr.Button("Сохранить", interactive=True, visible=False),# gr.Button("Сохранить",interactive=True, visible=True),
            gr.DownloadButton("Загрузить", interactive=True, visible=True, value=zipFilePath.name+'.zip'),# gr.DownloadButton("Загрузить", visible=False),
            gr.Button("Отправить на генерацию", interactive=True),
                []
                )
    if mode == "png":
        font = ImageFont.truetype(pathToFont, 50)
        images_out = []
        for key, text in m_dict.items():
            left, top, right, bottom = font.getbbox(text)
            width = right - left
            height = bottom - top
            img = Image.new("RGBA", (width, height))
            draw = ImageDraw.Draw(img)
            draw.text((0, -top), text, font=font, fill="#000000")
            images_out.append(img)
        convertImages = images_out
        gr.Info("Преобразование завершено!")
        logger.info("Done!")
        return (
                gr.Button("Сохранить",interactive=True), 
                gr.DownloadButton("Загрузить", visible=False),
                (gr.Button("Отправить на генерацию", interactive=True) if settings["IS_DEBUG"] else gr.Button("Отправить на генерацию", interactive=False)),
                images_out
                )
        
def saveImages(type: str, mode: str, path: str):
    logger.info(f"saveImages type = {type}, mode = {mode}")
    # cachePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache")
    zipFilePath = TemporaryFile()
    if mode == "png":
        zipFiles = []
        for i, cont in enumerate(convertImages):
            img_buffer = io.BytesIO()
            cont.save(img_buffer, 'PNG')
            img_buffer.seek(0)
            zipFiles.append((str(i)+'.'+type, img_buffer))
        zip = get_zip_buffer(zipFiles).getvalue()
        with open(zipFilePath.name+'.zip', 'wb') as f:   
            f.write(zip)
        return gr.Button("Сохранить", interactive=True, visible=False), gr.DownloadButton("Загрузить", interactive=True, visible=True, value=zipFilePath.name+'.zip')
    # if mode == "svg":
        # shutil.make_archive(zipFilePath, 'zip', os.path.join(cachePath, "svgFont2img"))
        # return gr.Button("Сохранить", interactive=True, visible=False), gr.DownloadButton("Загрузить", interactive=True, visible=True, value=zipFilePath)
        
def get_zip_buffer(list_of_tuples):
    zip_buffer = io.BytesIO()
    # https://gist.github.com/vulcan25/563808b415024925d2670b9381aa9763 <3
    # https://stackoverflow.com/a/44946732 <3   
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in list_of_tuples:
            zip_file.writestr(file_name, data.read())

    zip_buffer.seek(0)
    return zip_buffer

