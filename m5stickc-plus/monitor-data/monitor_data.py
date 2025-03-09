import matplotlib.pyplot as plt
import serial

class KalmanFilter:
    def __init__(self, F, G, H, Q, R):
        self.F = F
        self.G = G
        self.H = H
        self.Q = Q
        self.R = R
    
    def filter(self, x_prediction, P_prediction, y):
        K = P_prediction * self.H / (P_prediction * self.H ** 2 + self.R) # カルマンゲイン
        x_filtering = x_prediction + K * (y - self.H * x_prediction)
        P_filtering = P_prediction - K * self.H * P_prediction
        return (x_filtering, P_filtering)
    
    def predict(self, x_filtering, P_filtering):
        x_prediction = self.F * x_filtering
        P_prediction = (self.F ** 2) * P_filtering + (self.G ** 2) * self.Q
        return (x_prediction, P_prediction)

list_size_max = 100
acc_x_list = []
acc_y_list = []
acc_z_list = []

# 以下，Q, R および初期値は collect_data で収集したデータから計算
# R は机に置いた状態のデータの標本分散を使用 (Q が 0 の場合に相当)
# Q は手に置いた状態のデータの標本分散から R を引いたものを使用
#   y_t = H F x_{t - 1} + H G w_{t - 1} + v_t と書けるので，w_{t - 1} と v_t が独立であることから，
#   x_{t - 1} が得られたときの y_t の分散 V[y_t | x_{t - 1}] は w_{t - 1} の分散 Q と v_t の分散 R の和になる:
#   V[y_t | x_{t - 1}] = Q + R．よって，V[y_t | x_{t - 1}] を手に置いた状態のデータの標本分散で推定できるなら，
#   手に置いた状態のデータの標本分散から R を引いたものが Q の推定値となる．V[y_t | x_{t - 1}] を
#   そのように推定してよいのかという問題はあるが，ここでは目を瞑ることにする．
# 初期値の x_prediction は x, y 方向は 0.0 [G]，z 方向は 1.0 [G] とする (理論値を使用)
# 初期値の P_prediction は Q を使用

acc_x_Q = 0.000093
acc_x_kalman_filter = KalmanFilter(1.0, 1.0, 1.0, acc_x_Q, 0.000081)
(acc_x_x_prediction, acc_x_P_prediction) = (0.0, acc_x_Q) # 初期値
acc_x_x_filtering_list = []

acc_y_Q = 0.000103
acc_y_kalman_filter = KalmanFilter(1.0, 1.0, 1.0, acc_y_Q, 0.000062)
(acc_y_x_prediction, acc_y_P_prediction) = (0.0, acc_y_Q) # 初期値
acc_y_x_filtering_list = []

acc_z_Q = 0.000038
acc_z_kalman_filter = KalmanFilter(1.0, 1.0, 1.0, acc_z_Q, 0.000056)
(acc_z_x_prediction, acc_z_P_prediction) = (1.0, acc_z_Q) # 初期値
acc_z_x_filtering_list = []


# cf. [M5Stick-CからMacにBluetoothで文字列を送信する - plant-raspberrypi3のブログ](https://plant-raspberrypi3.hatenablog.com/entry/2020/12/14/232112)
# cf. [Pythonのpyserialとthreadingでリアルタイムなシリアル通信をする。 #電子工作 - Qiita](https://qiita.com/tapitapi/items/1dd9c66c0dff061bcd82)
port = '/dev/tty.M5StickCPlus' # NOTE 自分の環境に合わせて変更する
m5_stick_c_plus = serial.Serial(port, timeout=3)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
while True:
    line = m5_stick_c_plus.readline().strip().decode('utf-8')
    try:
        acc_data = [float(s) for s in line.split(',')]
    except ValueError as e:
        print('parse error:', e)
        break

    if len(acc_data) != 3:
        print('invalid accData')
        break

    acc_x = acc_data[0]
    acc_y = acc_data[1]
    acc_z = acc_data[2]

    # 観測更新
    (acc_x_x_filtering, acc_x_P_filtering) = acc_x_kalman_filter.filter(acc_x_x_prediction, acc_x_P_prediction, acc_x)
    (acc_y_x_filtering, acc_y_P_filtering) = acc_y_kalman_filter.filter(acc_y_x_prediction, acc_y_P_prediction, acc_y)
    (acc_z_x_filtering, acc_z_P_filtering) = acc_z_kalman_filter.filter(acc_z_x_prediction, acc_z_P_prediction, acc_z)

    print(f'acc_x: {acc_x} (filtering: {acc_x_x_filtering}), acc_y: {acc_y} (filtering: {acc_y_x_filtering}), acc_z: {acc_z} (filtering: {acc_z_x_filtering})')

    # 時間更新
    (acc_x_x_prediction, acc_x_P_prediction) = acc_x_kalman_filter.predict(acc_x_x_filtering, acc_x_P_filtering)
    (acc_y_x_prediction, acc_y_P_prediction) = acc_y_kalman_filter.predict(acc_y_x_filtering, acc_y_P_filtering)
    (acc_z_x_prediction, acc_z_P_prediction) = acc_z_kalman_filter.predict(acc_z_x_filtering, acc_z_P_filtering)

    acc_x_list.append(acc_x)
    if len(acc_x_list) > list_size_max:
        acc_x_list.pop(0)
    acc_y_list.append(acc_y)
    if len(acc_y_list) > list_size_max:
        acc_y_list.pop(0)
    acc_z_list.append(acc_z)
    if len(acc_z_list) > list_size_max:
        acc_z_list.pop(0)

    acc_x_x_filtering_list.append(acc_x_x_filtering)
    if len(acc_x_x_filtering_list) > list_size_max:
        acc_x_x_filtering_list.pop(0)
    acc_y_x_filtering_list.append(acc_y_x_filtering)
    if len(acc_y_x_filtering_list) > list_size_max:
        acc_y_x_filtering_list.pop(0)
    acc_z_x_filtering_list.append(acc_z_x_filtering)
    if len(acc_z_x_filtering_list) > list_size_max:
        acc_z_x_filtering_list.pop(0)

    time = range(len(acc_x_list))

    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax1.plot(time, acc_x_list, marker='', ls='-', color='blue')
    ax1.plot(time, acc_x_x_filtering_list, marker='', ls='--', color='orange')
    ax2.plot(time, acc_y_list, marker='', ls='-', color='red')
    ax2.plot(time, acc_y_x_filtering_list, marker='', ls='--', color='darkcyan')
    ax3.plot(time, acc_z_list, marker='', ls='-', color='green')
    ax3.plot(time, acc_z_x_filtering_list, marker='', ls='--', color='magenta')
    plt.pause(0.1)
