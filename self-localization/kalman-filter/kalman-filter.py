import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

rng = np.random.default_rng(736848565429029)
# rng = np.random.default_rng() # シードを固定しない場合はこちらを使用

class Robot:
    def __init__(self, Q: float, R: float, mean_x_0: float, Sigma: float):
        self.Q = Q
        self.R = R
        self.x = rng.normal(mean_x_0, Sigma)
        self.y = 0.0

    def move(self, u: float) -> None:
        self.x = self.x + u + rng.normal(0, self.Q)

    def observe(self) -> None:
        self.y = self.x + rng.normal(0, self.R)

robot = Robot(0.5, 2.0, 0.0, 0.5)

class KalmanFilter:
    def __init__(self, F: float, G: float, H: float, Q: float, R: float):
        self.F = F
        self.G = G
        self.H = H
        self.Q = Q
        self.R = R
    
    def filter(self, x_p: float, P_p: float, y: float) -> Tuple[float, float]:
        K = P_p * self.H / (P_p * (self.H ** 2) + self.R) # カルマンゲイン
        x_f = x_p + K * (y - self.H * x_p)
        P_f = P_p - K * self.H * P_p
        return (x_f, P_f)
    
    def predict(self, x_f: float, P_f: float, u: float) -> Tuple[float, float]:
        x_p = self.F * x_f + u
        P_p = (self.F ** 2) * P_f + (self.G ** 2) * self.Q
        return (x_p, P_p)

kalman_filter = KalmanFilter(1.0, 1.0, 1.0, 0.5, 2.0)

goal = 30.0
len_max = 35
x_list = []
y_list = []

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
y_min = -5.0
y_max = goal + 5.0

# 初期値
(x_p, P_p) = (0.0, 0.5)

# フィルタリング推定値のリスト
x_f_list = []

while True:
    x = robot.x
    x_list.append(x)
    if len(x_list) > len_max:
        x_list.pop(0)

    robot.observe()

    y = robot.y
    y_list.append(y)
    if len(y_list) > len_max:
        y_list.pop(0)

    # 観測更新
    (x_f, P_f) = kalman_filter.filter(x_p, P_p, y)

    x_f_list.append(x_f)
    if len(x_f_list) > len_max:
        x_f_list.pop(0)
    
    print(f'x: {x}, y: {y}, x_f: {x_f}')

    ax1.cla()
    ax1.vlines(x=0.0, ymin=y_min, ymax=y_max, color='black')
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(y_min, y_max)
    ax1.plot(0.0, x, marker='o', color='blue')
    ax1.plot(0.0, y, marker='x', color='red')
    ax1.plot(0.0, x_f, marker='d', color='green')

    ax2.cla()
    ax2.set_xlim(0, len_max)
    ax2.set_ylim(y_min, y_max)
    ax2.plot(range(len(x_list)), x_list, marker='o', ls='-', color='blue')
    ax2.plot(range(len(y_list)), y_list, marker='x', ls='--', color='red')
    ax2.plot(range(len(x_f_list)), x_f_list, marker='d', ls='-.', color='green')

    if y >= goal:
        print(f'goal! x: {x}, y: {y}')
        plt.show()
        break

    plt.pause(0.5)

    u = 1.0

    robot.move(u)

    # 時間更新
    (x_p, P_p) = kalman_filter.predict(x_f, P_f, u)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, len_max)
ax.set_ylim(y_min, y_max)
ax.plot(range(len(x_list)), x_list, marker='o', ls='-', color='blue')
ax.plot(range(len(y_list)), y_list, marker='x', ls='--', color='red')
ax.plot(range(len(x_f_list)), x_f_list, marker='d', ls='-.', color='green')
fig.savefig('state_observation_and_filtering')

ax.cla()
ax.set_xlim(0, len_max)
ax.set_ylim(y_min, y_max)
ax.plot(range(len(y_list)), y_list, marker='x', ls='--', color='red')
ax.plot(range(len(x_f_list)), x_f_list, marker='d', ls='-.', color='green')
fig.savefig('observation_and_filtering')

ax.cla()
ax.set_xlim(0, len_max)
ax.set_ylim(y_min, y_max)
ax.plot(range(len(x_list)), x_list, marker='o', ls='-', color='blue')
ax.plot(range(len(x_f_list)), x_f_list, marker='d', ls='-.', color='green')
fig.savefig('state_and_filtering')
