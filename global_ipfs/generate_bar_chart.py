import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# CSVデータ読み込み
df = pd.read_csv('global_ipfs/data.csv')

# グラフ作成
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df['region'], df['transfer_speed_mbps'], color='steelblue', edgecolor='black')

# 値ラベルを追加
for bar, speed in zip(bars, df['transfer_speed_mbps']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{speed:.2f}', ha='center', va='bottom', fontsize=16)

ax.set_xlabel('リージョン', fontsize=18)
ax.set_ylabel('平均転送速度 (Mbps)', fontsize=18)
ax.set_title('IPFSの地理的距離による転送速度', fontsize=20)
ax.set_ylim(0, 120)
ax.tick_params(axis='both', labelsize=16)
plt.tight_layout()

# PNG保存
plt.savefig('global_ipfs/bar_chart.png', dpi=150, bbox_inches='tight')
print("保存しました: global_ipfs/bar_chart.png")

# PDF保存
plt.savefig('global_ipfs/bar_chart.pdf', bbox_inches='tight')
print("保存しました: global_ipfs/bar_chart.pdf")
