import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np

filenames = ['prod-normal','prod-abnormal','eva-normal','eva-abnormal']

for filename in filenames:
    plt.figure()
    # タイトルの自動生成
    title = filename.split('-')
    if title[1] == 'normal':
        title = '地理的に近く、同じ時間に取得したデータ同士の相関係数の分布'
    elif title[1] == 'abnormal':
        title = '地理的に遠く、同じ時間に取得したデータ同士の相関係数の分布'
    # データの準備
    # ./prod-nomal.csvを読み込む
    data = np.loadtxt("./data/" + filename + '.csv', delimiter=',', dtype='float')

    # データの個数を取得
    total_data_count = len(data)

    bin_ranges = np.arange(0, 120, 12)
    # データを5の範囲でビンに分割 (Divide data into bins of range 5)
    hist, bins = np.histogram(data, bins=bin_ranges)

    # 0.2以上と以下で色を分けて棒グラフのプロット
    for i in range(len(hist)):
        if bins[i] >= 24:
            plt.bar(bins[i], hist[i], width=5, color='blue', align='edge')
        else:
            plt.bar(bins[i], hist[i], width=5, color='red', align='edge')

    # グラフのタイトルと軸ラベルの設定
    # plt.title(title)
    plt.xticks(np.arange(0, 120, 12))
    plt.yticks(np.arange(0, np.max(hist)+2, 2))
    plt.xlabel('DTW距離')
    plt.ylabel('データ数')

    plt.text(50, max(hist), f'総データ数: {total_data_count}', ha='center', va='bottom')


    # プロットの保存
    plt.savefig("./fig/dtw_" + filename + '.pdf')