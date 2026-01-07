import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
import pandas as pd

# データの読み込み
df_rapid = pd.read_csv('./zksnarks_rapid/rapidsnark.csv')
df_js = pd.read_csv('./zksnarks_js/zk_snarkjs.csv')

# Mac Dockerを除外
df_rapid = df_rapid[~df_rapid['デバイス'].isin(['Mac Docker'])]
df_js = df_js[~df_js['デバイス'].isin(['Mac Docker'])]

# デバイス名を短縮
def format_device_name(name):
    if 'Jetson Orin Nano(7W)' in name:
        return 'Jetson Orin\nNano(7W)'
    if 'Jetson Orin Nano(15W)' in name:
        return 'Jetson Orin\nNano(15W)'
    if 'RaspberryPi4' in name:
        return 'Raspberry\nPi4'
    if 'MacBook Pro' in name:
        return 'MacBook\nPro'
    if 'WSL' in name:
        return 'WSL\n(Ryzen7 7735HS)'
    return name

# 両方の最大値を計算して縦軸のスケールを揃える
max_rapid = max(df_rapid['Witness生成(秒)'].values + df_rapid['Proof生成(秒)'].values)
max_js = max(df_js['Witness生成(秒)'].values + df_js['Proof生成(秒)'].values)
y_max = max(max_rapid, max_js) * 1.2

def create_graph(df, title, filename):
    devices = df['デバイス'].values
    witness_times = df['Witness生成(秒)'].values
    proof_times = df['Proof生成(秒)'].values

    devices_formatted = [format_device_name(d) for d in devices]

    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(devices_formatted))
    width = 0.6

    # 積み上げ棒グラフ
    bars1 = ax.bar(x, witness_times, width, label='Witness生成', color='#4CAF50', edgecolor='black')
    bars2 = ax.bar(x, proof_times, width, bottom=witness_times, label='Proof生成', color='#FF9800', edgecolor='black')

    # 数値表示
    for i, (w, p) in enumerate(zip(witness_times, proof_times)):
        total = w + p
        # Witness部分
        if w > y_max * 0.06:
            ax.text(i, w/2, f'{w:.3f}', ha='center', va='center', fontsize=16, fontweight='bold', color='white')
        # Proof部分
        if p > y_max * 0.06:
            ax.text(i, w + p/2, f'{p:.3f}', ha='center', va='center', fontsize=16, fontweight='bold', color='white')
        # 合計
        ax.text(i, total + y_max * 0.02, f'{total:.3f}秒', ha='center', va='bottom', fontsize=18, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(devices_formatted)
    ax.set_xlabel('デバイス', fontsize=22, fontweight='bold')
    ax.set_ylabel('計算時間(秒)', fontsize=22, fontweight='bold')
    ax.tick_params(axis='both', labelsize=18)
    ax.set_ylim(0, y_max)
    ax.set_title(title, fontsize=26, fontweight='bold')
    ax.legend(fontsize=16, loc='upper right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(f'./{filename}.pdf')
    plt.savefig(f'./{filename}.png', dpi=150)
    plt.close()
    print(f'グラフを保存しました: ./{filename}.pdf, ./{filename}.png')

# rapidsnarkグラフ
create_graph(df_rapid, 'rapidsnark', 'zksnarks_rapidsnark')

# snarkjsグラフ
create_graph(df_js, 'snarkjs', 'zksnarks_snarkjs')

print(f'\n縦軸の最大値: {y_max:.2f}秒 (両グラフ共通)')
