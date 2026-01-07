import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np

# データの準備（サンプルデータ）
# 実際のデータファイルから読み込む場合は以下のようにコメントを外してください
# data = np.loadtxt("./data/scatter_data.csv", delimiter=',', dtype='float')
# x = data[:, 0]
# y = data[:, 1]

# サンプルデータの生成
np.random.seed(42)
x = np.random.randn(100)
y = 2 * x + np.random.randn(100) * 0.5

# 図の作成
plt.figure(figsize=(10, 6))

# 散布図のプロット
plt.scatter(x, y, c='blue', alpha=0.6, edgecolors='black', linewidth=0.5)

# 軸ラベルの設定
plt.xlabel('X軸')
plt.ylabel('Y軸')

# グリッドの表示
plt.grid(True, linestyle='--', alpha=0.7)

# プロットの保存
plt.savefig('./scatter_plot.pdf')
plt.savefig('./scatter_plot.png', dpi=300)

print("散布図を生成しました: scatter_plot.pdf, scatter_plot.png")
