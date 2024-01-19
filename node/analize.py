import numpy as np

filenames = ['jetsonNano','raspberryPi','macmini']

for filename in filenames:
    # データの準備
    data = np.loadtxt("./data/" + filename + '.csv', delimiter=',', dtype='float')

    # dataの平均と中央値と標準偏差を取得
    mean = np.mean(data)
    median = np.median(data)
    std = np.std(data)

    print(f'{filename}の平均: {mean}')
    print(f'{filename}の中央値: {median}')
    print(f'{filename}の標準偏差: {std}')