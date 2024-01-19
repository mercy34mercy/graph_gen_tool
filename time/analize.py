import numpy as np

filenames = ['dtw','corr']

for filename in filenames:
    # データの準備
    data = np.loadtxt("./data/" + filename + '.csv', delimiter=',', dtype='float')

    # dataの平均と中央値を取得
    mean = np.mean(data)
    median = np.median(data)

    print(f'{filename}の平均: {mean}')
    print(f'{filename}の中央値: {median}')