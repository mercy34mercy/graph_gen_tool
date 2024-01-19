import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np

filenames = ['jetsonNano','raspberryPi','macmini']

for filename in filenames:
    plt.figure()
    # データの準備
    data = np.loadtxt("./data/" + filename + '.csv', delimiter=',', dtype='float')

    bin_count = 10  # ビンの数を10に設定
    hist, bin_edges = np.histogram(data, bins=bin_count)

    # ヒストグラムのプロット
    plt.figure(figsize=(10, 6))
    plt.bar(bin_edges[:-1], hist, width=np.diff(bin_edges), edgecolor="black", align="edge")
    # plt.title(filename)
    plt.xlabel('計算時間(秒)')
    plt.ylabel('データ数(個)')


    # プロットの保存
    plt.savefig("./fig/" + filename + '.pdf')