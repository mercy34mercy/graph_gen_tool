import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 仮のデータ作成
np.random.seed(0)  # 再現性のためのシード
date_range = pd.date_range(start="2023-01-01", periods=200, freq="D")
values = np.cumsum(np.random.randn(200))  # ランダムな累積データ

# グラフの作成
plt.figure(figsize=(10, 6))
plt.plot(date_range, values, color='blue', linewidth=1)

# 軸目盛りを非表示にする
plt.xticks([])  # x軸の目盛りを非表示
plt.yticks([])  # y軸の目盛りを非表示

# グリッドと余白調整
plt.grid(True)
plt.tight_layout()

# グラフの保存
plt.savefig('test.png')

# グラフの表示
plt.show()
