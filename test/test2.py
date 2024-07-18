import numpy as np
from scipy.optimize import least_squares
from matplotlib import pyplot as plt

def bezier_curve(control_points, num_points):
    t = np.linspace(0, 1, num_points)
    bezier_points = np.zeros((num_points, 2))
    for i in range(num_points):
        bezier_points[i, 0] = (1 - t[i])**3 * control_points[0] + 3 * (1 - t[i])**2 * t[i] * control_points[1] + 3 * (1 - t[i]) * t[i]**2 * control_points[2] + t[i]**3 * control_points[3]
        bezier_points[i, 1] = (1 - t[i])**3 * control_points[4] + 3 * (1 - t[i])**2 * t[i] * control_points[5] + 3 * (1 - t[i]) * t[i]**2 * control_points[6] + t[i]**3 * control_points[7]
    return bezier_points

def residual(control_points, points):
    control_points = control_points.reshape(4, 2)
    bezier_points = bezier_curve(control_points.flatten(), len(points))
    return np.sqrt(np.sum((bezier_points - points)**2, axis=1))

def fit_bezier(points, endpoint1, endpoint2):
    control_points_init = np.array([endpoint1[0], endpoint1[1], endpoint1[0] + (endpoint2[0] - endpoint1[0])/3, endpoint1[1] + (endpoint2[1] - endpoint1[1])/3, endpoint2[0] - (endpoint2[0] - endpoint1[0])/3, endpoint2[1] - (endpoint2[1] - endpoint1[1])/3, endpoint2[0], endpoint2[1]])
    res = least_squares(residual, control_points_init, args=(points,))
    return res.x.reshape(4, 2)

# Example usage:
points = np.array([[0, 0], [1, 1], [2, 3]])
endpoint1 = [0, 0]
endpoint2 = [2, 3]
control_points = fit_bezier(points, endpoint1, endpoint2)
xpoints = [p[0] for p in points]
ypoints = [p[1] for p in points]
xcontrol_points = [p[0] for p in control_points]
ycontrol_points = [p[1] for p in control_points]
plt.plot(xpoints, ypoints)#, "ro")
plt.plot(xcontrol_points, ycontrol_points, "bo")
plt.show()
print(control_points)