---
marp: true
paginate: true
theme: default
math: mathjax
style: |
  {
    font-size:26px
  }
  section.centered {
    display: flex;
    justify-content: center;
  }
  section {
    display: flex;
    justify-content: center;
  }
  .blue {
    color: blue;
  }
  .red {
    color: red;
  }
  .green {
    color: green;
  }
---

# カルマンフィルタの紹介

katatoshi

---

## このスライドの目的

- カルマンフィルタはロボットの自己位置推定などで使われるアルゴリズム
- 簡単なロボットのシミュレーションを通して，カルマンフィルタについて紹介する

---

## カルマンフィルタの概要

- カルマンフィルタは
  - ロボットの自己位置推定
  - ロケットの軌道推定と軌道制御
  - リチウムイオン二次電池の状態推定
- などで使われるアルゴリズム
- カルマンフィルタを使うと，観測値から真の値を推定することができる
  - ロボットなら，目印からの距離の観測値から自身の位置を推定することができる

---

## 簡単なロボットの例: 初期位置

- 直線上を移動するロボット
- 最初に，ロボットを指定位置に設置しようとするが，指定位置が分かりにくい等の理由により，初期位置は指定位置からランダムにズレたものになる

![bg contain right:45%](IMG_9358.jpeg)

---

## 簡単なロボットの例: 観測

- ロボットは自分の位置は分からないが，目印からの距離を観測できる
- 目印からの距離の観測値には誤差があり，実際の距離からランダムにズレたものになる

![bg contain right:45%](IMG_9359.jpeg)

---

## 簡単なロボットの例: 移動

- ロボットは移動量を指令として受け取る
- ロボットは指令通り移動しようとするが，路面状況等により，指令からランダムにズレた位置に移動してしまう

![bg contain right:50%](IMG_9360.jpeg)

---

## 簡単なロボットのシミュレーション

- 簡単なロボットを Python でシミュレーション (simple_robot.py)
- ロボットは `Robot` クラスで表現
- 現在の位置 `x` と最新の観測値 `y` を属性として持つ

```python
class Robot

    def __init__(self, x_0: float, S: float, Q: float, R: float):
        w = rng.normal(0.0, S)
        self.x = x_0 + w
        self.y = 0.0
        self.Q = Q
        self.R = R
```

---

## ロボットの初期位置

```python
    def __init__(self, x_0: float, S: float, Q: float, R: float):
        w = rng.normal(0.0, S)
        self.x = x_0 + w
        self.y = 0.0
        self.Q = Q
        self.R = R
```
- `x_0` が指定位置
- `w` がランダムなズレ
  - `rng.normal(0.0, S)` は平均 `0.0`，分散 `S` の正規分布に従う乱数
  - 平均 `0.0` はどの辺りを中心にズレるのかを表している
  - 分散 `S` は中心からどれくらいズレ得るのかを表している

---

## 目印からの距離の観測

- `observe` メソッドで目印からの距離を観測する
```python
    def observe(self) -> None:
        v = rng.normal(0.0, self.R)
        self.y = self.x + v
```
- `v` が誤差を表すランダムなズレ
  - コンストラクタで定義していた属性 `R` は `v` の分散

---

## ロボットの移動

- `move` メソッドでロボットを移動させる
```python
    def move(self, u: float) -> None:
        w = rng.normal(0.0, self.Q)
        self.x = self.x + u + w
```
- `u` が指令 (移動量) で `w` がランダムなズレ
  - コンストラクタで定義していた属性 `Q` は `w` の分散

---

## シミュレーションの流れ

```python
# x_0=0.0, S=0.5 なので，初期位置は 0.0 周辺
# Q=0.5, R=2.0 なので，指令からのズレより観測誤差の方が大きい
robot = Robot(x_0=0.0, S=0.5, Q=0.5, R=2.0)
goal = 30.0 # ループを抜けるためにゴールを設定
while True:
    x = robot.x # ロボットの位置
    robot.observe() # 目印からの距離を観測させる
    y = robot.y # 目印からの距離の観測値
    if y >= goal: # 観測値でゴールに到達したか判断する
        break # ゴールを超えていたら終わり

    u = 1.0 # 1.0 移動するという指令
    robot.move(u) # 指令を渡してロボットを移動させる
```

---

## シミュレーションの実行

- simple_robot.py を実行すると...

---

## シミュレーションの結果

- 「<span class="blue">●︎</span>」(実線) がロボットの位置 `x`
- 「<span class="red">×</span>」(破線) が距離の観測値 `y`

![bg contain right:50%](self-localization/simple-robot/state_and_observation.png)

---

## 距離の観測値だけの結果

- 今回はシミュレーションなのでロボットの位置がわかっているが，実際には，距離の観測値しか分からない
- ロボットの位置は距離の観測値から推定するしかない

![bg contain right:50%](self-localization/simple-robot/only_observation.png)

---

## カルマンフィルタでロボットの位置を推定

- 今回の簡単なロボットのような動きをするものには，カルマンフィルタを使うことができる
- カルマンフィルタを使うと，距離の観測値からロボットの位置を推定することができる

---

## カルマンフィルタの実行

- kalman_filter.py は simple_robot.py にカルマンフィルタの実装を追加したもの
- kalman_filter.py を実行すると...

---

## カルマンフィルタの結果

- 「<span class="blue">●</span>」(実線) がロボットの位置
- 「<span class="red">×</span>」(破線) が距離の観測値
- 「<span class="green">♦︎</span>」(鎖線) がカルマンフィルタの推定値

![bg contain right:50%](self-localization/kalman-filter/state_observation_and_filtering.png)

---

## ロボットの位置と推定値

- カルマンフィルタの推定値はロボットの位置をよく再現している
- この推定値の計算にロボットの位置は使っていない

![bg contain right:50%](self-localization/kalman-filter/state_and_filtering.png)

---

## 距離の観測値と推定値

- カルマンフィルタの推定値は観測値の大きな動きを押さえたような動きをしている

![bg contain right:50%](self-localization/kalman-filter/observation_and_filtering.png)

---

## カルマンフィルタのアルゴリズム

- カルマンフィルタでは，ロボットの位置の**事前推定値**と**事後推定値**という，2つの推定値が登場する
- この2つの推定値を交互に更新しながら，ロボットの位置を推定していく
- 「カルマンフィルタの推定値」と呼んでいたものは，事後推定値の方

---

## カルマンフィルタ: 初期化

- ロボットが設置された直後は，指定位置 $x_0$ しかないので，これを事前推定値 $x_p$ の初期値とする

![bg contain right:45%](IMG_9361.jpeg)

---

## カルマンフィルタ: 事後推定値

- 観測値 $y$ が得られたら，事前推定値 $x_p$ と合わせて，事後推定値 $x_f$ を計算，更新する
- 観測値が得られた後だから「事後」

![bg contain right:50%](IMG_9362.jpeg)

---

## カルマンフィルタ: 事前推定値

- 指令 (移動量) $u$ が与えられたら，事後推定値 $x_f$ から次の事前推定値 $x_f$ を計算，更新する
- 観測値が得られる前だから「事前」

![bg contain right:50%](IMG_9363.jpeg)

---

## カルマンフィルタの実装

- kalman_filter.py
- カルマンフィルタは `KalmanFilter` クラスで実装
- 事前推定値 `x_p` と事後推定値 `x_f` を属性として持つ
  - `P_p` は事前推定誤差，`P_f` は事後推定誤差を表す
```python
class KalmanFilter

    def __init__(self, x_0: float, S: float, Q: float, R: float):
        self.x_p = x_0
        self.P_p = S
        self.x_f = 0.0
        self.P_f = 0.0
        self.Q = Q
        self.R = R
```

---

## カルマンフィルタの初期化

```python
    def __init__(self, x_0: float, S: float, Q: float, R: float):
        self.x_p = x_0
        self.P_p = S
        self.x_f = 0.0
        self.P_f = 0.0
        self.Q = Q
        self.R = R
```
- コンストラクタの引数には，ロボットと同じ値が入ることを想定している
- 事前推定値 `x_p` を指定位置 `x_0` で初期化する
  - 事前推定誤差 `P_p` は指定位置からのズレの分散 `S` で初期化する

---

## 事後推定値の更新

- `filter` メソッドで事後推定値を更新する
```python
    def filter(self, y: float) -> None:
        K = self.P_p / (self.P_p + self.R)
        self.x_f = self.x_p + K * (y - self.x_p)
        self.P_f = self.P_p - K * self.P_p
```
- 観測値 `y` と事前推定値 `x_p` から事後推定値 `x_f` を計算して更新する
  - 計算式の意味は補足を参照
- `K` はカルマンゲインと呼ばれる

---

## 事前推定値の更新

- `predict` メソッドで事後推定値を更新する
```python
    def predict(self, u: float) -> None:
        self.x_p = self.x_f + u
        self.P_p = self.P_f + self.Q
```
- 指令 `u` と事後推定値 `x_f` から事前推定値 `x_p` を計算して更新する
- 事後推定値 `x_f` から指令 `u` だけ進んだ位置を，次の事前推定値 `x_p` としているだけ

---

## カルマンフィルタのアルゴリズムの流れ

```python
robot = Robot(x_0=0.0, S=0.5, Q=0.5, R=2.0)
# robot と同じパラメータの値で kalman_filter を作る
kalman_filter = KalmanFilter(x_0=0.0, S=0.5, Q=0.5, R=2.0)
goal = 30.0
while True:
    x = robot.x
    x_p = kalman_filter.x_p # 事前推定値
    robot.observe()
    y = robot.y
    kalman_filter.filter(y) # 観測値が得られたので事後推定値を更新
    x_f = kalman_filter.x_f # 事後推定値
    if y >= goal:
        break

    u = 1.0
    robot.move(u)
    kalman_filter.predict(u) # 指令を渡して事前推定値を更新
```

---

## 発展的な話題

- TODO 修正予定
- 予測推定値とフィルタリング推定値の更新でやっていることについて説明したが，あの更新式でうまく推定できることの裏付けは，数学的により厳密に説明できる
  - 元々，そっちが気になって勉強していた
- このスライドで「カルマンフィルタが適用できる状況」，「真の値」と呼んでいたものは，一般的には「状態空間モデル」，「状態」とそれぞれ呼ばれる
- 今回，$y = x + v, x' = x + u + w$ という状況を考えたが，より一般に，$F, G, H$ を定数として，$y = H x + v, x' = F x + u + G w$ といった状況もカルマンフィルタで扱える
- 今回は1次元のケースを扱ったが，多次元のケースも扱える (むしろほとんどの場合そう)

---

## カルマンフィルタの限界

- TODO 修正予定
- カルマンフィルタは $y = H x + v, x' = F x + u + G w$ という状況にも適用できると述べたが，さらに一般化して，$h$, $f$ を関数として，$y = h(x) + v, x' = f(x, u) + G w$ という状況を考えると，一般に，これはカルマンフィルタでは扱うことができるとは限らない
  - 例えば，$y = x^2 + v, x' = \sin(x) + w$ という状況は扱えない
- こういった状況には，拡張カルマンフィルタやパーティクルフィルタといった，近似的な手法を適用することができる
  - 平面を動くロボットを考えると，こういった状況をなってしまうため，必然的に，拡張カルマンフィルタやパーティクルフィルタなどの手法を使う必要がある
  - 拡張カルマンフィルタとパーティクルフィルタについても勉強したので機会があれば説明したい

---

## まとめ

- TODO 修正予定
- カルマンフィルタが適用できる状況では，カルマンフィルタを使うことで，雑音を含む観測値から真の値を推定することができる
- カルマンフィルタでは予測推定値とフィルタリング推定値の2つの推定値を交互に更新することで，真の値を推定している
- 予測推定値は真の値の推移法則を利用して，次の真の値を推定している
- フィルタリング推定値は前回の予測推定値という今ある情報と，観測値という新しく得られた情報を，その信頼度に応じた割合で取り込むことで，現在の真の値を推定している
- カルマンフィルタは係数が1でないケースや多次元のケースにも適用できる
- カルマンフィルタが適用できないような状況もあるが，そのような状況には，拡張カルマンフィルタやパーティクルフィルタといった手法が適用できる

---

## 参考文献

- 足立 修一，丸田 一郎『カルマンフィルタの基礎』東京電機大学出版局，2012
- 上田 隆一『詳解 確率ロボティクス Pythonによる基礎アルゴリズムの実装』講談社，2019
- 片山 徹『非線形カルマンフィルタ』朝倉書店，2011
- 片山 徹「非線形カルマンフィルタの基礎」計測と制御，2017年56巻9号 p.638-643
  - https://www.jstage.jst.go.jp/article/sicejl/56/9/56_638/_pdf/-char/ja (pdf)
- 野村 俊一『カルマンフィルタ―Rを使った時系列予測と状態空間モデル―』共立出版，2016
