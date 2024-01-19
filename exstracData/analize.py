import numpy as np

filenames = ['ipfs']

for filename in filenames:
    # データの準備
    data = np.loadtxt("./data/" + filename + '.csv', delimiter=',', dtype='float')

    # dataの平均と中央値を取得
    mean = np.mean(data)
    median = np.median(data)
    std_dev = np.std(data)

    print(f'{filename}の平均: {mean}')
    print(f'{filename}の中央値: {median}')
    print(f'{filename}の標準偏差: {std_dev}')