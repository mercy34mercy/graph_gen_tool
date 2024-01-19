import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np

filenames = ['dtw','corr']

for filename in filenames:
    plt.figure()
    # データの準備
    data = np.loadtxt("./data/" + filename + '.csv', delimiter=',', dtype='float')

    if filename == 'dtw':
        titile = 'DTW距離の計算時間の分布'
    elif filename == 'corr':
        titile = '相関係数の計算時間の分布'

    bin_count = 10  # ビンの数を10に設定
    hist, bin_edges = np.histogram(data, bins=bin_count)

    # ヒストグラムのプロット
    plt.figure(figsize=(10, 6))
    plt.bar(bin_edges[:-1], hist, width=np.diff(bin_edges), edgecolor="black", align="edge")
    # plt.title(titile)
    plt.xlabel('計算時間(秒)')
    plt.ylabel('データ数(個)')


    # プロットの保存
    plt.savefig("./fig/" + filename + '.pdf')