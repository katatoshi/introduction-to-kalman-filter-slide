import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(736848565429029)
# rng = np.random.default_rng() # シードを固定しない場合はこちらを使用

class SimpleRobot:
    """直線上を移動する簡単なロボット

    observe → move → observe → move → ... のように observe と move を交互に呼んで，ロボットを動かす．

    Attributes
    ----------
    x: float
        ロボットの位置
    y: float
        距離の観測値
    Q: float
        ロボットが移動するときの指令からのズレの分散
    R: float
        観測誤差の分散
    """

    def __init__(self, x_0: float, S: float, Q: float, R: float):
        """
        Parameters
        ----------
        x_0: float
            初期位置の指定値
        S: float
            初期位置の指定値からのズレの分散
        Q: float
            ロボットが移動するときの指令からのズレの分散
        R: float
            観測誤差の分散
        """
        self.x = x_0 + rng.normal(0.0, S)
        self.y = 0.0 # まだ何も観測していないということ (0.0 という値に意味はない)
        self.Q = Q
        self.R = R

    def observe(self) -> None:
        """距離を観測する

        距離の観測値が更新される．
        """
        v = rng.normal(0.0, self.R)
        self.y = self.x + v

    def move(self, u: float) -> None:
        """指令 (移動量) を受け取って移動する

        ロボットの位置が更新される．

        Parameters
        ----------
        u: float
            指令 (移動量)
        """
        w = rng.normal(0.0, self.Q)
        self.x = self.x + u + w

# x_0=0.0, S=0.5 で，初期位置は 0.0 周辺であることを表す
# Q=0.5, R=2.0 で，移動時のズレに比べて，観測値の誤差が大きいことを表す
simple_robot = SimpleRobot(x_0=0.0, S=0.5, Q=0.5, R=2.0)

goal = 30.0 # ループを抜けるためにゴールを設定

len_max = 35
x_list = []
y_list = []
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
y_min = -5.0
y_max = goal + 5.0

while True:
    # ここが移動後のタイミング (初回は初期位置に設置されたタイミング)

    x = simple_robot.x # ロボットの位置

    x_list.append(x)
    if len(x_list) > len_max:
        x_list.pop(0)

    simple_robot.observe() # 距離を観測させる
    y = simple_robot.y # 距離の観測値

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

    if y >= goal: # 実際には，ロボットには真の位置が分からないので，観測値でゴールに到達したか判断
        print(f'goal! x: {x}, y: {y}')
        plt.show()
        break # ゴールを超えているなら終わり

    plt.pause(0.5)

    u = 1.0 # 1.0 移動せよという指令
    simple_robot.move(1.0) # 指令を渡して移動させる

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
