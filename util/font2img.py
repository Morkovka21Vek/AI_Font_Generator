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
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# https://github.com/mathandy/svgpathtools
from libs.svgpathtools import (wsvg, Line, CubicBezier, QuadraticBezier, Path)

logger = logging.getLogger("app.util.font2img")

convertImages = []

# def font2img_start(pathToFont: str, mode: str, settings):
#     out = font2img(pathToFont, mode, settings)
#     out

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
    if mode == "svg":
        shutil.rmtree(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache'))
        os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache', 'svgFont2img'))
        converter = TtfSvgConverter(ttfPath=pathToFont)
        for key, text in m_dict.items():
            converter.generate(text, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache", "svgFont2img", str(key)+".svg"))
        gr.Info("Преобразование завершено!")
        logger.info("Done!")
        return (
                gr.Button("Сохранить",interactive=True, visible=True),
                gr.DownloadButton("Загрузить", visible=False),
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
    cachePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache")
    zipFilePath = os.path.join(cachePath, "downloadZip.zip")
    if mode == "png":
        zipFiles = []
        for i, cont in enumerate(convertImages):
            img_buffer = io.BytesIO()
            cont.save(img_buffer, 'PNG')
            img_buffer.seek(0)
            zipFiles.append((str(i)+'.'+type, img_buffer))
        zip = get_zip_buffer(zipFiles).getvalue()
        with open(zipFilePath, 'wb') as f:   
            f.write(zip)
        return gr.Button("Сохранить", interactive=True, visible=False), gr.DownloadButton("Загрузить", interactive=True, visible=True, value=zipFilePath)
    if mode == "svg":
        shutil.make_archive(os.path.join(cachePath, "downloadZip"), 'zip', os.path.join(cachePath, "svgFont2img"))
        return gr.Button("Сохранить", interactive=True, visible=False), gr.DownloadButton("Загрузить", interactive=True, visible=True, value=zipFilePath)
        
def get_zip_buffer(list_of_tuples):
    zip_buffer = io.BytesIO()
    # https://gist.github.com/vulcan25/563808b415024925d2670b9381aa9763 <3
    # https://stackoverflow.com/a/44946732 <3   
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in list_of_tuples:
            zip_file.writestr(file_name, data.read())

    zip_buffer.seek(0)
    return zip_buffer

# https://gist.github.com/GaryLee/04dd0537fc501724b0f3af329864bcf1 <3
class TtfSvgConverter:
    VERBOSE = False
    STROKE_WIDTHS = 10
    CHAR_WIDTH = 48
    CHAR_HEIGHT = 64
    CHAR_SIZE = CHAR_WIDTH * CHAR_HEIGHT
    def __init__(self, ttfPath=None):
        self.ttfPath = ttfPath
        self.reset()

    def reset(self):
        self.svgPath = []
        self._lastX = 0
        self._lastY = 0

    def _verbose(self, *args):
        if self.VERBOSE:
            print(*args)

    def lastXyToComplex(self):
        return self.tupleToComplex((self._lastX, self._lastY))

    def tupleToComplex(self, xy):
        return xy[0] + xy[1] * 1j

    def vectorToComplex(self, v):
        return v.x + v.y * 1j

    def vectorsToPoints(self, vectors):
        return [(v.x, v.y) for v in vectors if v is not None]

    def callbackMoveTo(self, *args):
        self._verbose('MoveTo ', len(args), self.vectorsToPoints(args))
        self._lastX, self._lastY = args[0].x, args[0].y

    def callbackLineTo(self, *args):
        self._verbose('LineTo ', len(args), self.vectorsToPoints(args))
        line = Line(self.lastXyToComplex(), self.vectorToComplex(args[0]))
        self.svgPath.append(line)
        self._lastX, self._lastY = args[0].x, args[0].y

    def callbackConicTo(self, *args):
        self._verbose('ConicTo', len(args), self.vectorsToPoints(args))
        curve = QuadraticBezier(self.lastXyToComplex(), self.vectorToComplex(args[0]), self.vectorToComplex(args[1]))
        self.svgPath.append(curve)
        self._lastX, self._lastY = args[1].x, args[1].y

    def callbackCubicTo(self, *args):
        self._verbose('CubicTo', len(args), self.vectorsToPoints(args))
        curve = CubicBezier(self.lastXyToComplex(), self.vectorToComplex(args[0]), self.vectorToComplex(args[1]), self.vectorToComplex(args[2]))
        self.svgPath.append(curve)
        self._lastX, self._lastY = args[2].x, args[2].y

    def calcViewBox(self, path):
        xmin, xmax, ymin, ymax = path.bbox()
        xmin, xmax, ymin, ymax = xmin - self.CHAR_WIDTH, xmax + self.CHAR_WIDTH, ymin - self.CHAR_HEIGHT, ymax + self.CHAR_HEIGHT
        dx = xmax - xmin
        dy = ymax - ymin
        viewbox = '{} {} {} {}'.format(xmin, ymin, dx, dy)
        return viewbox

    def generate(self, text, output):
        self.reset()
        face = Face(self.ttfPath)
        face.set_char_size(self.CHAR_SIZE)
        for ch in text:
            face.load_char(ch)
            outline = face.glyph.outline
            outline.decompose(context=None, move_to=self.callbackMoveTo, line_to=self.callbackLineTo, conic_to=self.callbackConicTo, cubic_to=self.callbackCubicTo)
            path = Path(*self.svgPath).scaled(1, -1)
            viewbox = self.calcViewBox(path)
            attr = {
                'width': '100%',
                'height': '100%',
                'viewBox': viewbox,
                'preserveAspectRatio': 'xMidYMid meet'
            }
            #MODE
            #0-save stroke
            #1-save fill
            #2-nosave stroke
            #3-nosave fill
            wsvg(paths=path, colors=['#000000'], svg_attributes=attr, filename=output, mode=1)
            # with open(output, "r") as f:
            #     text = f.read().replace(' fill="none" stroke="#000000" ', '').split("stroke-width")[0]+"/>\n</svg>"
                
            # with open(output, "w") as f:
            #     f.write(text)
            break 
