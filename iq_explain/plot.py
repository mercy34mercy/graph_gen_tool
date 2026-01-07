import matplotlib.pyplot as plt
import numpy as np

# ダミーのIQデータを生成
samples = 300
I = np.random.randn(samples)
Q = np.random.randn(samples)

# 時系列プロット
plt.figure(figsize=(12, 6))

# I成分のプロット
plt.subplot(2, 1, 1)
plt.plot(I, color='blue')
plt.title('I Component')
plt.xlabel('Date')
plt.ylabel('Amplitude')

# Q成分のプロット
plt.subplot(2, 1, 2)
plt.plot(Q, color='green')
plt.title('Q Component')
plt.xlabel('Date')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.savefig('iq_data_plot.png')
