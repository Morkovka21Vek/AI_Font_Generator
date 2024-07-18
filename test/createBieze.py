import numpy as np
from scipy.special import comb
from svg.path import parse_path
from xml.dom import minidom

def extract_path(name, freq, freq2, freq3, scale=1, x_offset=0, y_offset=0):
    doc = minidom.parse(name)
    path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    doc.unlink()

    path = []
    path2 = []
    path3 = []
    bezier_curve1000 = []
    bezier_curve3 = []
    # for path_string in path_strings:
    #     items = parse_path(path_string)
    #     for item in items:
    #         leng = item.length()
    #         step = int(leng/freq)
    #         for time in range(step):
    #             time/=step
    #             pos = item.point(time)
    #             path.append([(pos.real+x_offset)*scale, (pos.imag+y_offset)*scale])
    
    for path_string in path_strings:
        items = parse_path(path_string)
        step = len(items)*len(path_strings)/freq
        step2 = len(items)*len(path_strings)/freq2
        step3 = len(items)*len(path_strings)/freq3
        print(len(items), len(path_strings), step, step2, step3)
        for item in items:
            for i in range(int(1/step)):
                pos = item.point(step*i)
                path.append([(pos.real+x_offset)*scale, (pos.imag+y_offset)*scale])
                path3 = []
                path3.append([(pos.real+x_offset)*scale, (pos.imag+y_offset)*scale])
                for i3 in range(int(step/step3)):
                    pos3 = item.point(step*i+step3*i3)
                    # print(step*i, step3*i3, step*i+step3*i3)
                    path3.append([(pos3.real+x_offset)*scale, (pos3.imag+y_offset)*scale])
                path3 = np.array(path3)
                # path3 = (path3-np.min(path3))/(np.max(path3)-np.min(path3))
                # path3 = path3 * 200
                bezier_curve1000.append(bezier_curve(path3, nTimes=1000))
                bezier_curve3.append(bezier_curve(path3, nTimes=3))
                    
                
            for i in range(int(1/step2)):
                pos = item.point(step2*i)
                path2.append([(pos.real+x_offset)*scale, (pos.imag+y_offset)*scale])

    return path, path3, bezier_curve1000, bezier_curve3

def bernstein_poly(i, n, t):
    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i


def bezier_curve(points, nTimes=1000):
    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    
    path, path2, bezier_curve1000, bezier_curve3 = extract_path("training\\trainingDataset\\Van Helsing__65.svg", 100, 300, 500)
    print(len(path), len(path2), len(bezier_curve1000))
    path = np.array(path)
    # path = (path-np.min(path))/(np.max(path)-np.min(path))
    # path = path * 200
    
    path2 = np.array(path2)
    # path2 = (path2-np.min(path2))/(np.max(path2)-np.min(path2))
    # path2 = path2 * 200
    
    # path3 = np.array(path3)
    # path3 = (path3-np.min(path3))/(np.max(path3)-np.min(path3))
    # path3 = path3 * 200
    # print(path)
    
    xpoints = [p[0] for p in path]
    ypoints = [p[1] for p in path]
    
    xpoints2 = [p[0] for p in path2]
    ypoints2 = [p[1] for p in path2]

    # xvals, yvals = bezier_curve(path3, nTimes=1000)
    # xvals3, yvals3 = bezier_curve(path3, nTimes=3)
    print(len(bezier_curve1000), len(bezier_curve3))
    for i1, i2 in zip(bezier_curve1000, bezier_curve3):
        # print(i1[0])
        plt.plot(i1[0], i1[1], "g")
        plt.plot(i2[0], i2[1], "m")
    # plt.plot(xvals3, yvals3)
    plt.plot(xpoints2, ypoints2, "bo")
    plt.plot(xpoints, ypoints, "ro")
    plt.show()