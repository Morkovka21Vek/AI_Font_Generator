import numpy as np
from scipy.special import comb
from svg.path import parse_path
from xml.dom import minidom
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline

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
    points = [[0, 0], [1, 1], [2, 3]]
    xpoints = [p[0] for p in points]
    ypoints = [p[1] for p in points]

    xvals, yvals = bezier_curve(points, nTimes=1000)
    p0 = np.array([xvals[0], yvals[0]])
    p3 = np.array([xvals[-1], yvals[-1]])
    t = np.linspace(0, 1, len(xvals))
    spl = make_interp_spline(t, np.c_[xvals, yvals], k=3)
    t_mid = 0.5
    p1 = spl(t_mid)
    p2 = 1 * spl(t_mid) - spl(2 * t_mid)
    xvals1, yvals1 = bezier_curve([p0, p2, p3], nTimes=1000)
    # xvals3, yvals3 = bezier_curve(path3, nTimes=3)
    plt.plot(xvals, yvals)
    plt.plot(xvals1, yvals1, "g")
    plt.plot(xpoints, ypoints, "ro")
    # plt.plot(p1[0], p1[1], "bo")
    plt.plot(p2[0], p2[1], "bo")
    plt.show()