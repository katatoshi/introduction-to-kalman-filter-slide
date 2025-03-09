import math
import matplotlib.pyplot as plt
import numpy as np
import serial

# M5StickC Plus の MPU6866 の値を Bluetooth で受信してデータを集める
# 収集例:
#
# list_size_max = 300
#
# 机の上
#
# 標本平均:
# mean_acc_x: -0.021590
# mean_acc_y: -0.007404
# mean_acc_z: 1.083106
#
# 標本分散
# var_acc_x: 0.000081
# var_acc_y: 0.000062
# var_acc_z: 0.000056
#
# 手の上
#
# 標本平均
# mean_acc_x: -0.103458
# mean_acc_y: -0.033325
# mean_acc_z: 1.071780
#
# 標本分散
# var_acc_x: 0.000174
# var_acc_y: 0.000165
# var_acc_z: 0.000094

list_size_max = 300
acc_x_list = []
acc_y_list = []
acc_z_list = []

# cf. [M5Stick-CからMacにBluetoothで文字列を送信する - plant-raspberrypi3のブログ](https://plant-raspberrypi3.hatenablog.com/entry/2020/12/14/232112)
# cf. [Pythonのpyserialとthreadingでリアルタイムなシリアル通信をする。 #電子工作 - Qiita](https://qiita.com/tapitapi/items/1dd9c66c0dff061bcd82)
port = '/dev/tty.M5StickCPlus' # NOTE 自分の環境に合わせて変更する
m5_stick_c_plus = serial.Serial(port, timeout=3)
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
    print(f'acc_x:{acc_x},acc_y:{acc_y},acc_z:{acc_z}')
    acc_x_list.append(acc_x)
    acc_y_list.append(acc_y)
    acc_z_list.append(acc_z)
    if list_size_max < len(acc_x_list):
        break
m5_stick_c_plus.close()

acc_x_data = np.array(acc_x_list)
acc_y_data = np.array(acc_y_list)
acc_z_data = np.array(acc_z_list)

mean_acc_x = np.mean(acc_x_data)
mean_acc_y = np.mean(acc_y_data)
mean_acc_z = np.mean(acc_z_data)
print('mean:')
print(f'    mean_acc_x: {mean_acc_x:f}')
print(f'    mean_acc_y: {mean_acc_y:f}')
print(f'    mean_acc_z: {mean_acc_z:f}')

var_acc_x = np.var(acc_x_data, ddof=1)
var_acc_y = np.var(acc_y_data, ddof=1)
var_acc_z = np.var(acc_z_data, ddof=1)
print('var:')
print(f'    var_acc_x: {var_acc_x:f}')
print(f'    var_acc_y: {var_acc_y:f}')
print(f'    var_acc_z: {var_acc_z:f}')

bins = math.floor(math.log2(len(acc_x_data)) + 1) # スタージェスの公式
print(f'bins: {bins}')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
ax1.hist(acc_x_data, bins=bins, density=True, orientation="horizontal", color='blue')
ax2.hist(acc_y_data, bins=bins, density=True, orientation="horizontal", color='red')
ax3.hist(acc_z_data, bins=bins, density=True, orientation="horizontal", color='green')
plt.show()
