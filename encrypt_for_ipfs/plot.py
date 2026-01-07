import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import japanize_matplotlib

# CSVからデータを読み込み
df = pd.read_csv('./benchmark_data.csv')

devices_raw = df['device'].tolist()
encryption_times = df['total_encrypt_avg_ms'].tolist()  # ms
decryption_times = df['total_decrypt_avg_ms'].tolist()  # ms

# デバイス名を改行して横幅を制限
def format_device_name(name):
    # Jetson Orin Nano(xW) → Jetson Orin Nano\n(xW)
    if 'Jetson Orin Nano' in name:
        return name.replace('Jetson Orin Nano', 'Jetson Orin Nano\n')
    return name

devices = [format_device_name(d) for d in devices_raw]

# 棒グラフの設定
x = np.arange(len(devices))
width = 0.35

fig, ax = plt.subplots(figsize=(16, 7))
bars1 = ax.bar(x - width/2, encryption_times, width, label='暗号化', color='#4CAF50', edgecolor='black')
bars2 = ax.bar(x + width/2, decryption_times, width, label='複合', color='#2196F3', edgecolor='black')

# 棒の上に数値を表示
for bar in bars1:
    height = bar.get_height()
    if height >= 1000:
        label = f'{height/1000:.2f}s'
    else:
        label = f'{height:.0f}ms'
    ax.text(bar.get_x() + bar.get_width()/2, height + 50,
            label, ha='center', va='bottom', fontsize=20, fontweight='bold')

for bar in bars2:
    height = bar.get_height()
    if height >= 1000:
        label = f'{height/1000:.2f}s'
    else:
        label = f'{height:.0f}ms'
    ax.text(bar.get_x() + bar.get_width()/2, height + 50,
            label, ha='center', va='bottom', fontsize=20, fontweight='bold')

# 軸ラベルとフォントサイズ設定
ax.set_xlabel('デバイス', fontsize=24, fontweight='bold')
ax.set_ylabel('処理時間 (ms)', fontsize=24, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(devices, fontsize=20, ha='center')
ax.tick_params(axis='y', labelsize=20)
ax.set_ylim(0, max(max(encryption_times), max(decryption_times)) * 1.15)
ax.legend(fontsize=20, loc='upper left')

# グリッドを追加
ax.grid(axis='y', linestyle='--', alpha=0.7)

# プロットの保存
plt.tight_layout()
plt.savefig('./fig/benchmark.pdf')
plt.savefig('./fig/benchmark.png', dpi=300)
print('グラフを保存しました: ./fig/benchmark.pdf, ./fig/benchmark.png')

# ================================================================================
# 2つ目のグラフ: ECDH計算時間とAES暗号化時間の内訳（積み上げ棒グラフ）
# ================================================================================

# ECDH時間（usからmsに変換）とAES時間（ms）
ecdh_encrypt_ms = [x / 1000 for x in df['ecdh_encrypt_avg_us'].tolist()]
aes_encrypt_ms = df['aes_encrypt_avg_ms'].tolist()
ecdh_decrypt_ms = [x / 1000 for x in df['ecdh_decrypt_avg_us'].tolist()]
aes_decrypt_ms = df['aes_decrypt_avg_ms'].tolist()

fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 7))

# 暗号化の内訳
bars_aes_enc = ax1.bar(x, aes_encrypt_ms, width=0.6, label='AES暗号化', color='#4CAF50', edgecolor='black')
bars_ecdh_enc = ax1.bar(x, ecdh_encrypt_ms, width=0.6, bottom=aes_encrypt_ms, label='ECDH計算', color='#FFC107', edgecolor='black')

ax1.set_xlabel('デバイス', fontsize=20, fontweight='bold')
ax1.set_ylabel('処理時間 (ms)', fontsize=20, fontweight='bold')
ax1.set_title('暗号化時間の内訳', fontsize=22, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(devices, fontsize=16, ha='center')
ax1.tick_params(axis='y', labelsize=16)
ax1.legend(fontsize=16, loc='upper left')
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# 各バーの上に合計時間を表示
for i, (aes, ecdh) in enumerate(zip(aes_encrypt_ms, ecdh_encrypt_ms)):
    total = aes + ecdh
    if total >= 1000:
        label = f'{total/1000:.2f}s'
    else:
        label = f'{total:.0f}ms'
    ax1.text(i, total + max(encryption_times) * 0.02, label, ha='center', va='bottom', fontsize=14, fontweight='bold')

# 復号化の内訳
bars_aes_dec = ax2.bar(x, aes_decrypt_ms, width=0.6, label='AES複合', color='#2196F3', edgecolor='black')
bars_ecdh_dec = ax2.bar(x, ecdh_decrypt_ms, width=0.6, bottom=aes_decrypt_ms, label='ECDH計算', color='#FFC107', edgecolor='black')

ax2.set_xlabel('デバイス', fontsize=20, fontweight='bold')
ax2.set_ylabel('処理時間 (ms)', fontsize=20, fontweight='bold')
ax2.set_title('複合時間の内訳', fontsize=22, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(devices, fontsize=16, ha='center')
ax2.tick_params(axis='y', labelsize=16)
ax2.legend(fontsize=16, loc='upper left')
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# 各バーの上に合計時間を表示
for i, (aes, ecdh) in enumerate(zip(aes_decrypt_ms, ecdh_decrypt_ms)):
    total = aes + ecdh
    if total >= 1000:
        label = f'{total/1000:.2f}s'
    else:
        label = f'{total:.0f}ms'
    ax2.text(i, total + max(decryption_times) * 0.02, label, ha='center', va='bottom', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('./fig/benchmark_breakdown.pdf')
plt.savefig('./fig/benchmark_breakdown.png', dpi=300)
print('グラフを保存しました: ./fig/benchmark_breakdown.pdf, ./fig/benchmark_breakdown.png')
