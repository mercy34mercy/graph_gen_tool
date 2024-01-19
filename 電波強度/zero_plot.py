import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import sys

# 313の長さのall0の配列を作成
plot_data_1 = np.zeros(313)
plot_data_2 = np.zeros(313)

plt.figure()

# data1_1とdata2_1をプロット
plt.plot(plot_data_1, lw=4 ,label='機器1')
plt.plot(plot_data_2,lw=4, label='機器2')

for i in plot_data_1:
    if i < 0:
        print(i)
for i in plot_data_2:
    if i < 0:
        print(i)


# x軸とy軸のラベルを追加
plt.xlabel("時間(秒)",fontsize=18,fontweight='bold')
plt.ylabel("電波強度",fontsize=18,fontweight='bold')
# タイトルと凡例を追加
# plt.title(f"時間ごとの電波強度の変化({'1775.5MHz〜1777MHz'}) \n 相関係数:{1}, DTW距離:{0}")
plt.legend()

# x軸とy軸の範囲を設定 (必要に応じて調整してください)
plt.xlim([0, len(plot_data_1)])  # 例えば、データポイント数に合わせて調整
plt.ylim(0,1)  # 最小値と最大値を基に範囲を設定

# ファイルに保存
plt.savefig('./fig/fft_' + 'all_zero' + '.pdf')
