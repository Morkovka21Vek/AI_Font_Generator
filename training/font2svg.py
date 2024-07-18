from fontTools.ttLib import TTFont
from freetype import Face, FT_Curve_Tag, FT_Curve_Tag_On, FT_Vector

import os
# import logging
import string
from tqdm import tqdm

import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# https://github.com/mathandy/svgpathtools
from libs.svgpathtools import (wsvg, Line, CubicBezier, QuadraticBezier, Path)

cyrillic_lower_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
desiredLetters = string.ascii_uppercase + cyrillic_lower_letters.upper()
# desiredLetters = list(string.ascii_uppercase) + list(cyrillic_lower_letters.upper())
desiredLetters = [ord(i) for i in desiredLetters]


def font2img(pathToFont: str, fontName: str):
    font_obg = TTFont(pathToFont)
    m_dict = font_obg.getBestCmap()
    converter = TtfSvgConverter(ttfPath=pathToFont)
    for key, text in m_dict.items():
        if key in desiredLetters:
            converter.generate(text, os.path.join(os.path.dirname(os.path.abspath(__file__)), "trainingDataset", f"{fontName}__{str(key)}.svg"))
        
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
            wsvg(paths=path, colors=['#000000'], svg_attributes=attr, filename=output)
            # with open(output, "r") as f:
            #     text = f.read().replace(' fill="none" stroke="#000000" ', '').split("stroke-width")[0]+"/>\n</svg>"
                
            # with open(output, "w") as f:
            #     f.write(text)
            break 
        
if __name__ == "__main__":
    folderFontPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trainingFonts")
    listFonts = os.listdir(folderFontPath)
    fullListFonts = [os.path.join(folderFontPath, i) for i in listFonts]
    # print(fullListFonts)
    for fontPath, fontName in tqdm(zip(fullListFonts, listFonts), total=len(fullListFonts)):
        font2img(fontPath, fontName.rsplit('.', 1)[0])
