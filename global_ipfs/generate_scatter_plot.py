import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# CSVデータ読み込み
df = pd.read_csv('global_ipfs/data.csv')

# グラフ作成
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df['distance_km'], df['transfer_speed_mbps'], s=150, c='steelblue', edgecolors='black')

# 各点の上にリージョン名を追加（東京は下に配置）
for i, row in df.iterrows():
    if row['region'] == '東京':
        ax.annotate(row['region'], (row['distance_km'], row['transfer_speed_mbps']),
                    textcoords="offset points", xytext=(0, -20), ha='center', fontsize=20)
    else:
        ax.annotate(row['region'], (row['distance_km'], row['transfer_speed_mbps']),
                    textcoords="offset points", xytext=(0, 15), ha='center', fontsize=20)

ax.set_xlabel('地理的距離 (km)', fontsize=22)
ax.set_ylabel('平均転送速度 (Mbps)', fontsize=22)
# ax.set_title('IPFSの地理的距離による転送速度', fontsize=24)
ax.tick_params(axis='both', labelsize=20)
ax.grid(True, alpha=0.3)
plt.tight_layout()

# PNG保存
plt.savefig('global_ipfs/scatter_plot.png', dpi=150, bbox_inches='tight')
print("保存しました: global_ipfs/scatter_plot.png")

# PDF保存
plt.savefig('global_ipfs/scatter_plot.pdf', bbox_inches='tight')
print("保存しました: global_ipfs/scatter_plot.pdf")
