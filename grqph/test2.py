import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 仮のデータ作成
np.random.seed(0)  # 再現性のためのシード
date_range = pd.date_range(start="2023-01-01", periods=300, freq="D")
I_values = np.random.randn(300)  # ランダムデータ (I Component)
Q_values = np.random.randn(300)  # ランダムデータ (Q Component)

# グラフの作成
fig, axs = plt.subplots(2, 1, figsize=(12, 6), sharex=True)  # 2行1列のサブプロット

# I Componentのグラフ
axs[0].plot(date_range, I_values, color='blue', linewidth=1)
axs[0].grid(True)

# Q Componentのグラフ
axs[1].plot(date_range, Q_values, color='green', linewidth=1)
axs[1].grid(True)

plt.xticks([])  # x軸の目盛りを非表示
plt.yticks([])  # y軸の目盛りを非表示
# 余白調整と表示
plt.tight_layout()
plt.savefig('test2.png')
