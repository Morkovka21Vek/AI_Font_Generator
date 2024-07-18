import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Функция для построения квадратичной кривой Безье
def build_bezier_curve(control_points):
    x = control_points[:, 0]
    y = control_points[:, 1]

    t = np.linspace(0, 1, 100)
    curve_x = np.power(1 - t, 2) * x[0] + 2 * (1 - t) * t * x[1] + t * t * x[2]
    curve_y = np.power(1 - t, 2) * y[0] + 2 * (1 - t) * t * y[1] + t * t * y[2]

    return curve_x, curve_y

# Функция для нахождения контрольных точек квадратичной кривой Безье
def find_control_points(points):
    x = points[:, 0]
    y = points[:, 1]

    t = np.linspace(0, 1, len(points))
    x_polynomial = interp1d(t, x, kind='cubic')
    y_polynomial = interp1d(t, y, kind='cubic')

    t_new = np.linspace(0, 1, 3)
    control_points_x = np.array([x_polynomial(t_) for t_ in t_new]).reshape((3, 1))
    control_points_y = np.array([y_polynomial(t_) for t_ in t_new]).reshape((3, 1))

    control_points = np.hstack((control_points_x, control_points_y))
    return control_points

# Зададим наши точки
points = np.array([[0, 0], [1, 1], [2, 1], [2, 2]])

# Найдем контрольные точки
control_points = find_control_points(points)
print("Контрольные точки:", control_points)

# Построим кривую Безье
curve_x, curve_y = build_bezier_curve(control_points)
print(curve_x, curve_y)
# Визуализация
plt.plot(curve_x, curve_y)
# plt.plot(points[0], points[1])
# plt.plot(points[1], points[2])
plt.plot(points[:, 0], points[:, 1], "ro")

plt.show()