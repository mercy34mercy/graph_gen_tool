import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np

# MacBook Pro 1MBデータのベンチマーク結果
# ECDH時間 (us -> ms)
ecdh_encrypt = 59 / 1000  # 0.059 ms
ecdh_decrypt = 56 / 1000  # 0.056 ms

# AES時間 (ms)
aes_encrypt = 1.0  # ms
aes_decrypt = 1.0  # ms

# 総時間
total_encrypt = ecdh_encrypt + aes_encrypt
total_decrypt = ecdh_decrypt + aes_decrypt

# 割合計算
ecdh_enc_ratio = (ecdh_encrypt / total_encrypt) * 100
aes_enc_ratio = (aes_encrypt / total_encrypt) * 100
ecdh_dec_ratio = (ecdh_decrypt / total_decrypt) * 100
aes_dec_ratio = (aes_decrypt / total_decrypt) * 100

print(f"暗号化: ECDH {ecdh_enc_ratio:.2f}%, AES {aes_enc_ratio:.2f}%")
print(f"復号化: ECDH {ecdh_dec_ratio:.2f}%, AES {aes_dec_ratio:.2f}%")

# ================================================================================
# 積み上げ棒グラフ（割合表示）
# ================================================================================
fig, ax = plt.subplots(figsize=(10, 7))

categories = ['暗号化', '復号化']
ecdh_ratios = [ecdh_enc_ratio, ecdh_dec_ratio]
aes_ratios = [aes_enc_ratio, aes_dec_ratio]

x = np.arange(len(categories))
width = 0.5

# 積み上げ棒グラフ
bars_aes = ax.bar(x, aes_ratios, width, label='AES暗号化/復号化', color='#4CAF50', edgecolor='black')
bars_ecdh = ax.bar(x, ecdh_ratios, width, bottom=aes_ratios, label='ECDH計算', color='#FFC107', edgecolor='black')

# 割合をバー内に表示
for i, (aes_r, ecdh_r) in enumerate(zip(aes_ratios, ecdh_ratios)):
    # AES部分
    ax.text(i, aes_r / 2, f'{aes_r:.1f}%\n({aes_encrypt:.2f}ms)',
            ha='center', va='center', fontsize=18, fontweight='bold', color='white')
    # ECDH部分
    ax.text(i, aes_r + ecdh_r / 2, f'{ecdh_r:.1f}%\n({ecdh_encrypt*1000:.0f}μs)',
            ha='center', va='center', fontsize=14, fontweight='bold')

ax.set_ylabel('処理時間の割合 (%)', fontsize=20, fontweight='bold')
ax.set_title('MacBook Pro (1MBデータ) 暗号化処理の内訳', fontsize=22, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=20)
ax.tick_params(axis='y', labelsize=16)
ax.set_xlim(-0.8, 1.8)
ax.set_ylim(0, 100)
ax.legend(fontsize=16, loc='lower right')
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('./fig/ratio_1mb.pdf')
plt.savefig('./fig/ratio_1mb.png', dpi=300)
print('グラフを保存しました: ./fig/ratio_1mb.pdf, ./fig/ratio_1mb.png')
