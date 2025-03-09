import numpy as np
import matplotlib.pyplot as plt

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

goal = 30.0
len_max = 35
x_list = []
y_list = []

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
y_min = -5.0
y_max = goal + 5.0

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
    
    print(f'x: {x}, y: {y}')

    ax1.cla()
    ax1.vlines(x=0.0, ymin=y_min, ymax=y_max, color='black')
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(y_min, y_max)
    ax1.plot(0.0, x, marker='o', color='blue')
    ax1.plot(0.0, y, marker='x', color='red')

    ax2.cla()
    ax2.set_xlim(0, len_max)
    ax2.set_ylim(y_min, y_max)
    ax2.plot(range(len(x_list)), x_list, marker='o', ls='-', color='blue')
    ax2.plot(range(len(y_list)), y_list, marker='x', ls='--', color='red')

    if y >= goal:
        print(f'goal! x: {x}, y: {y}')
        plt.show()
        break

    plt.pause(0.5)

    u = 1.0

    robot.move(u)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, len_max)
ax.set_ylim(y_min, y_max)
ax.plot(range(len(x_list)), x_list, marker='o', ls='-', color='blue')
ax.plot(range(len(y_list)), y_list, marker='x', ls='--', color='red')
fig.savefig('state_and_observation')

ax.cla()
ax.set_xlim(0, len_max)
ax.set_ylim(y_min, y_max)
ax.plot(range(len(y_list)), y_list, marker='x', ls='--', color='red')
fig.savefig('only_observation')
