
import numpy as np
import matplotlib.pyplot as plt


# Входные параметры
A1 = 642
A2 = -0.35
R = A1 / 2
C = 321.852
D_SV = 105
y = np.linspace(0, D_SV / 2, 500)
D0 = 45
S = 480
delta = 50

# Расчет параметров ближайшей сферы по четырем точкам:

y1 = D0 / 2
y2 = D_SV / 2
y3 = (y2 + y1) / 2
print(f'----------------------\n'
      f'y1: {y1}\ny2: {y2}\ny3: {y3}')

x1 = (-(np.sqrt(-(4 * A2 * (y1 ** 2)) + A1 ** 2)) + A1) / (2 * A2)
x2 = (-(np.sqrt(-(4 * A2 * (y2 ** 2)) + A1 ** 2)) + A1) / (2 * A2)
x3 = (x2 + x1) / 2
print(f'----------------------\n'
      f'x1: {x1}\nx2: {x2}\nx3: {x3}')

tanFI = (y2 - y1) / (x2 - x1)
print(f'----------------------\n'
      f'tan_fi: {tanFI}')
print(f'tan_fi (сам угол): {np.arctan(tanFI)*180/np.pi}')
print(f'----------------------')
C = y3 * tanFI + x3
print(f'C: {C}')

R = np.sqrt(((y3 ** 2) * (1 + tanFI ** 2)) + ((y2 - y1) ** 2 + (x2 - x1) ** 2) / 4)
print(f'R: {R}')

# Нахождение точек "Х" АП и ближайшей сферы с построением графиков:

X_ap = (-(np.sqrt(-(4 * A2 * (y ** 2)) + A1 ** 2)) + A1) / (2 * A2)
X_blig_sf = (C) - np.sqrt(R ** 2 - y ** 2)

# plt.title('Графики Асферической поверхности и ближайшей сферы')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.minorticks_on()
# plt.grid(which='minor', alpha=0.2)
# plt.grid(which='major', alpha=0.5)
# plt.plot(X_ap, y, linewidth = 2)
# plt.plot(X_blig_sf, y, linewidth = 1)
# plt.legend(['График АП', 'График ближайшей сферы'])
# plt.show()

# Расчет толщины наносимого слоя:

t = -X_blig_sf + X_ap
# очищаю толщину от отрицательных значений
t_izm = []
for tolsh in t:
    if tolsh < 0:
        t_izm.append(0)
    else:
        t_izm.append(tolsh)
t = t_izm
del t_izm

#нахождение градиента асферичности - изменение толщины асферичности на 1 мм.
print(f'----------------------\n'
      f'Градиент асферичности: {round((t[t.index(max(t))]-t[t.index(max(t))-10])/1, 6)}')
# print('/////////////////////////')
# print(round(y[475], 2))
# print(round(t[475], 5))
# print('/////////////////////////')
print(f'----------------------\n'
      f'Толщина наносимого слоя: {t}')

# plt.title('График толщины наносимого слоя')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.minorticks_on()
# plt.grid(which='minor', alpha=0.2)
# plt.grid(which='major', alpha=0.5)
# plt.plot(t, y, linewidth=2)
# # plt.legend(['График АП', 'График ближайшей сферы'])
# plt.show()

# Максимальное значение толщины:
t_max = max(t)
print(f'Максимальная толщина наносимого слоя: {round(t_max, 6)}')

# Рассчет коэффициента к1:

x = []
for _ in y:
    x.append(R - np.sqrt(R ** 2 - _ ** 2))
print(f'----------------------\n'
      f'Координата Х ОД для расчета маски: {x}')

fi_max = 1.3962634016  # радиан или 80 градусов
x_max = R - np.sqrt(R ** 2 - max(y) ** 2)
u_max = -((np.arctan(max(y) / (x_max - S))))
way_max = (np.arcsin(max(y) / R))
r_max = ((delta - S) * max(y)) / (x_max - S)

print(f'----------------------\n'
      f'Максимальный угол раскрытия: {fi_max} радиан')
print(f'Максимальное значение Х: {x_max}')
print(f'Максимальное значение u: {u_max} радиан')
print(f'Максимальное значение way: {way_max} радиан')
print(f'Максимальное значение r: {r_max}')

k1 = ((t_max * (delta - S) * (x_max - S)) / (fi_max * np.cos(u_max - way_max))) * ((r_max / (delta - S)) ** 2 + 1)
print(f'----------------------\n'
      f'Коэффициент к1:{k1}')

# Расчет fi углов маски:
fi_ = []
R_fi = []

for _ in range(0, 500):
    r0 = (y[_] * (delta - S)) / (x[_] - S)
    h0 = t[_]
    u0 = np.arctan(y[_] / (x[_] - S))
    way0 = np.arcsin(y[_] / R)
    fi = (((h0 * (delta - S) * (x[_] - S)) / (k1 * np.cos(u0 - way0))) * ((r0 / (delta - S)) ** 2 + 1))
    if fi > 0:
        fi_.append(fi)
        R_fi.append(r0)
        plt.polar(fi + (90 * np.pi * 0 / 180), r0, 'r.')
        plt.polar(fi + (90 * np.pi * 1 / 180), r0, 'r.')
        plt.polar(fi + (90 * np.pi * 2 / 180), r0, 'r.')
        plt.polar(fi + (90 * np.pi * 3 / 180), r0, 'r.')

print(f'----------------------\n'
      f'Радиус векторы для углов: {R_fi}')
print(f'Углы: {fi_}')

# чертеж маски

plt.minorticks_on()
plt.grid(which='minor', alpha=0.2)
plt.grid(which='major', alpha=0.5)
plt.title('Чертеж маски')
plt.show()

