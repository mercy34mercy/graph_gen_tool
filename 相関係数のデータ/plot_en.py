import matplotlib.pyplot as plt
import numpy as np

filenames = ['prod-normal', 'prod-abnormal', 'eva-normal', 'eva-abnormal']

for filename in filenames:
    # タイトルの自動生成
    title = filename.split('-')
    if title[1] == 'normal':
        title = '地理的に近く、同じ時間に取得したデータ同士の相関係数の分布'
    elif title[1] == 'abnormal':
        title = '地理的に遠く、同じ時間に取得したデータ同士の相関係数の分布'

    # データの準備
    data = np.loadtxt("./data/" + filename + '.csv', delimiter=',', dtype='float')

    # データの個数を取得
    total_data_count = len(data)

    # ビンの設定
    bin_ranges = np.arange(0, 1.05, 0.05)  # Include 1.0
    hist, bins = np.histogram(data, bins=bin_ranges)

    # グラフ作成
    fig, ax = plt.subplots(figsize=(10, 6))

    # 棒グラフをプロット（色分け）
    for i in range(len(hist)):
        color = 'blue' if bins[i] >= 0.2 else 'red'
        ax.bar(bins[i], hist[i], width=0.05, color=color, align='edge')

    # 0.2の基準線を引く
    ax.axvline(x=0.2, color='black', linestyle='--', linewidth=5.5)

    # グラフの設定
    ax.set_xticks(np.arange(0, 1.1, 0.1))
    ax.set_yticks(np.arange(0, max(hist) + 2, 2))
    ax.tick_params(axis='both', labelsize=24)
    ax.set_xlabel('Correlation Coefficient', fontsize=24, fontweight='bold')
    ax.set_ylabel('Number of Data Points', fontsize=24, fontweight='bold')

    # 合計データ数を表示
    # 枠線を追加
    ax.text(0.8, max(hist) * 0.95, f'Total Data Count: {total_data_count}', fontsize=24, ha='center', va='top', backgroundcolor='white', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    # グリッドを追加
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # プロットの保存
    plt.tight_layout()
    plt.savefig(f"./fig/en/corr_{filename}.pdf")
    plt.close()
