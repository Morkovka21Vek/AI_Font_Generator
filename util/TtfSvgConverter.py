from svgpathtools import (wsvg, Line, CubicBezier, QuadraticBezier, Path)
from freetype import Face, FT_Curve_Tag, FT_Curve_Tag_On, FT_Vector
from svgwrite import Drawing

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

    def generate(self, text, output, mode=0):
        self.reset()
        face = Face(self.ttfPath)
        face.set_char_size(self.CHAR_SIZE)
        for ch in text:
            face.load_char(ch)
            outline = face.glyph.outline
            outline.decompose(context=None, move_to=self.callbackMoveTo, line_to=self.callbackLineTo, conic_to=self.callbackConicTo, cubic_to=self.callbackCubicTo)
            path = Path(*self.svgPath).scaled(1, -1)
            if self.svgPath == []:
                print(output)
                return None
            # print(path, self.svgPath, end="\n\n\n\n")
            viewbox = self.calcViewBox(path)
            # attr = {
            #     'width': '100%',
            #     'height': '100%',
            #     'viewBox': viewbox,
            #     'preserveAspectRatio': 'xMidYMid meet'
            # }
            
            #MODE
            #0-save
            #1-nosave
            dwg = Drawing(filename=output, viewBox=viewbox, size=('100%', '100%'), preserveAspectRatio='xMidYMid meet')
            for i, p in enumerate([path]):
                ps = p.d()#Path(p).d()

                dwg.add(dwg.path(ps, stroke='#000000', stroke_width=str(2))) #, fill='none'
            # print(dwg)
            if mode == 0:
                dwg.save()
            elif mode == 1:
                return dwg.tostring()
            else:
                pass
            # return wsvg(paths=path, colors=['#000000'], svg_attributes=attr, filename=output, mode=mode)
            break 