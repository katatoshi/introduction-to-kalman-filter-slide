import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(736848565429029)
# rng = np.random.default_rng() # シードを固定しない場合はこちらを使用

class Robot:
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
            初期位置の指定位置
        S: float
            初期位置の指定位置からのズレの分散
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

# x_0=0.0, S=0.5 なので，初期位置は 0.0 周辺
# Q=0.5, R=2.0 なので，指令からのズレより観測誤差の方が大きい
robot = Robot(x_0=0.0, S=0.5, Q=0.5, R=2.0)

class KalmanFilter:
    """カルマンフィルタ

    filter → predict → filter → predict → ... のように filter と predict を交互に呼んで，ロボットの位置 (ロボットの場合は位置) の推定値を更新していく．

    Attributes
    ----------
    x_p: float
        ロボットの位置の事前推定値．次の観測値を得る前に，次の位置を推定しているので「事前」という
    P_p: float
        ロボットの位置の事前推定誤差の分散．次の位置が，その事前推定値 x_p から，どれくらい外れ得るか (誤差) を表す
    x_f: float
        ロボットの位置の事後推定値．現在の観測値を得た後に，現在の位置を推定しているので「事後」という
    P_f: float
        ロボットの位置の事後推定誤差の分散．現在の位置が，その事後推定値 x_f から，どれくらい外れ得るか (誤差) を表す
    Q: float
        ロボットの位置が推移するときの指令からのズレの分散
    R: float
        観測誤差の分散
    """

    def __init__(self, x_0: float, S: float, Q: float, R: float):
        """
        Parameters
        ----------
        x_0: float
            初期位置の指定位置
        S: float
            初期位置の指定位置からのズレの分散
        Q: float
            ロボットが移動するときの指令からのズレの分散
        R: float
            観測誤差の分散
        """
        self.x_p = x_0
        self.P_p = S
        self.x_f = 0.0 # まだ何もフィルタリングしていないということ (0.0 という値に意味はない)
        self.P_p = 0.0 # まだ何もフィルタリングしていないということ (0.0 という値に意味はない)
        self.Q = Q
        self.R = R
    
    def filter(self, y: float) -> None:
        """観測値を受け取って事後推定値を更新する

        事後推定値 x_f と事後推定誤差 P_f が更新される．

        Parameters
        ----------
        y: float
            観測値
        """
        K = self.P_p / (self.P_p + self.R) # カルマンゲイン
        self.x_f = self.x_p + K * (y - self.x_p)
        self.P_f = self.P_p - K * self.P_p
    
    def predict(self, u: float) -> None:
        """指令 (推移量) を受け取って事前推定値を更新する

        事前推定値 x_p と事前推定誤差 P_p が更新される．

        Parameters
        ----------
        u: float
            指令 (推移量)
        """
        self.x_p = self.x_f + u
        self.P_p = self.P_f + self.Q

# robot と同じパラメータの値で kalman_filter を作る
kalman_filter = KalmanFilter(x_0=0.0, S=0.5, Q=0.5, R=2.0)

goal = 30.0 # ループを抜けるためにゴールを設定

len_max = 35
x_list = []
y_list = []
x_f_list = []

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
y_min = -5.0
y_max = goal + 5.0

t = 0 # 時点
t_list = []
while True:
    t_list.append(t)
    if len(t_list) > len_max:
        t_list.pop(0)

    x = robot.x # ロボットの位置

    x_list.append(x)
    if len(x_list) > len_max:
        x_list.pop(0)

    # x_p = kalman_filter.x_p # ロボットの位置の事前推定値

    robot.observe() # 目印からの距離を観測させる
    y = robot.y # 目印からの距離の観測値

    y_list.append(y)
    if len(y_list) > len_max:
        y_list.pop(0)

    kalman_filter.filter(y) # 観測値が得られたので事後推定値を更新
    x_f = kalman_filter.x_f # ロボットの位置の事後推定値

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
    ax2.plot(range(len(t_list)), t_list, marker='', color='black')
    ax2.plot(range(len(x_list)), x_list, marker='o', ls='-', color='blue')
    ax2.plot(range(len(y_list)), y_list, marker='x', ls='--', color='red')
    ax2.plot(range(len(x_f_list)), x_f_list, marker='d', ls='-.', color='green')

    if x_f >= goal: # 事後推定値でゴールに到達したか判断する
        print(f'goal! x: {x}, y: {y}, x_f: {x_f}')
        plt.show()
        break # ゴールを超えていたら終わり

    plt.pause(0.5)

    # u = 1.0 # 1.0 移動するという指令
    u = (t + 1) - x_f # 次の t + 1 時点では t + 1 の位置に移動してほしいので，事後推定値から指令を計算
    robot.move(u) # 指令を渡してロボットを移動させる
    kalman_filter.predict(u) # 指令を渡して事前推定値を更新
    t += 1

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
