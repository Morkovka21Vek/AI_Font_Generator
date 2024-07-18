from svg.path import parse_path
from xml.dom import minidom
#(data-np.min(data))/(np.max(data)-np.min(data))

# https://ru.stackoverflow.com/questions/1071720/Получение-пути-построения-из-svg <3
def extract_path(name, freq, scale=1, x_offset=0, y_offset=0):
    doc = minidom.parse(name)
    path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    doc.unlink()

    path = []

    for path_string in path_strings:
        items = parse_path(path_string)
        for item in items:
            leng = item.length()
            step = round(leng/freq)
            for time in range(step):
                time/=step
                pos = item.point(time)
                path.append([(pos.real+x_offset)*scale, (pos.imag+y_offset)*scale])

    return path

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    import numpy as np
    path = extract_path("training\\trainingDataset\\Van Helsing__65.svg", 100)
    path = np.array(path)
    path = (path-np.min(path))/(np.max(path)-np.min(path))
    path = path * 500
    img = Image.new('RGB', (500, 500), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for x, y in path:
        draw.ellipse((x-2, y-2, x+2, y+2), fill='black')
    print(path)
    img.save("out.png")
    img.show()