import matplotlib.pyplot as plt
import numpy as np

# 初期値を設定
initial_value = 0

# ランダムウォークデータを生成 (各ステップで前の値にランダムな変化を加える)
random_walk = [initial_value]
for _ in range(1, 200):
    random_walk.append(random_walk[-1] + np.random.randn())
# 時系列データをプロット
plt.figure(figsize=(10, 6))
plt.plot(random_walk,color='orange')
plt.xlabel('Date')
plt.ylabel('Value')
plt.grid(True)
plt.tick_params(labelbottom=False, labelleft=False)

plt.savefig('random_walk_1.png')


# ランダムウォークデータを生成 (各ステップで前の値にランダムな変化を加える)
random_walk = [initial_value]
for _ in range(1, 200):
    random_walk.append(random_walk[-1] + np.random.randn())
# 時系列データをプロット
plt.figure(figsize=(10, 6))
plt.plot(random_walk, color='blue')
plt.xlabel('Date')
plt.ylabel('Value')
# メモリの数字を表示しない
plt.tick_params(labelbottom=False, labelleft=False)
plt.grid(True)

plt.savefig('random_walk_2.png')