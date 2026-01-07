
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import sys
from fastdtw import fastdtw

sample_rate = 10e6

# プロットするデータセット
plot_file_path = [
            ['data2_1720_11-14_17-42-30.npy','data3_1720_11-14_17-42-30.npy','1720.5MHz〜1722MHz','near_serial_1'],
            ['data2_1720_11-14_17-25-30.npy','data3_1720_11-14_17-25-30.npy','1720.5MHz〜1722MHz','near_serial_2'],
            # ['data2_1775_11-14_17-39-30.npy','data3_1775_11-14_17-39-30.npy','1775.5MHz〜1777MHz','near_serial_3'],
            # ['data2_1775_11-14_17-45-30.npy','data3_1775_11-14_17-45-30.npy','1775.5MHz〜1777MHz','near_serial_4'],
            ['data2_1950_11-14_17-22-30.npy','data3_1950_11-14_17-22-30.npy','1950.5MHz〜1952MHz','near_discon_1'],
            ['data2_1950_11-14_17-39-30.npy','data3_1950_11-14_17-39-30.npy','1950.5MHz〜1952MHz','near_discon_2'],
        ]

plot_far_file_path = [
            ['data2_1720_11-14_17-42-30.npy','data3_1720_11-14_17-28-30.npy','1720.5MHz〜1722MHz','far_serial_1'],
            ['data2_1720_11-14_17-25-30.npy','data3_1720_11-14_17-19-30.npy','1720.5MHz〜1722MHz','far_serial_2'],
            ['data2_1950_11-14_17-22-30.npy','data3_1950_11-14_17-16-30.npy','1950.5MHz〜1952MHz','far_discon_1'],
            ['data2_1950_11-14_17-39-30.npy','data3_1950_11-14_17-19-30.npy','1950.5MHz〜1952MHz','far_discon_2'],
        ]   

def dtw_distance(data1, data2):
    # fastdtwを用いてDTW距離を計算
    data1 = np.array(data1)
    data2 = np.array(data2)

    distance, path = fastdtw(data1, data2)
    return distance


def pearson_correlation_coefficient(X, Y):
    """ピアソンの相関係数を計算する
    
    Args:
    - X (list or numpy.array): データセットX
    - Y (list or numpy.array): データセットY

    Returns:
    float: ピアソンの相関係数
    """

    min_length = min(len(X), len(Y))
    
    X = X[:min_length]
    Y = Y[:min_length]
    
    # 共分散
    cov_XY = np.cov(X, Y, bias=False)[0][1]
    
    # X, Y の標準偏差
    std_X = np.std(X)
    std_Y = np.std(Y)
    
    # ピアソンの相関係数
    if std_X * std_Y == 0:
        return 0
    correlation_coefficient = cov_XY / (std_X * std_Y)
    
    return correlation_coefficient

def max_shifted_correlation(X, Y, shift=10):
    """左右に最大10ステップずつずらしながら最高の相関係数とそのシフト量を計算する

    Args:
    - X (list or numpy.array): データセットX
    - Y (list or numpy.array): データセットY
    - shift (int): 最大シフト量

    Returns:
    float: 最も高い相関係数
    int: そのときのシフト量
    """
    max_corr = float('-inf')
    max_shift = 0  # 最高の相関係数を持つシフト量
    len_X = len(X)
    len_Y = len(Y)

    for s in range(-shift, shift + 1):
        if abs(s) >= min(len_X, len_Y):
            continue

        if s < 0:
            corr = pearson_correlation_coefficient(X[:s], Y[-s:])
        elif s > 0:
            corr = pearson_correlation_coefficient(X[s:], Y[:-s])
        else:
            corr = pearson_correlation_coefficient(X, Y)

        if np.isfinite(corr) and corr > max_corr:
            max_corr = corr
            max_shift = s

    if max_corr == float('-inf'):
        max_corr = 0

    return max_corr, max_shift

# 正規化を行う
def normalize(data1,data2):

    ## 正規化を行う
    data1_max = max(data1)
    data1_min = min(data1)
    data2_max = max(data2)
    data2_min = min(data2)

    data_max = max(max(data1), max(data2))
    data_min = min(min(data1), min(data2))

    ## np.arrayに変換
    data1 = np.array(data1)
    data2 = np.array(data2)


    ## dataの最大値と最小値が3dB以下の場合、すなわち通信が行われていない場合、そのまま正規化すると無駄なノイズを比べることになるので、0にする
    ## それ以外の場合は正規化する
    if data1_max - data1_min < 3:
        normalized_array_1[:] = 0
    else:
        # 正規化を行う
        normalized_array_1 = (data1 - data_min) / (data_max - data_min)
        normalized_array_1[normalized_array_1 < 0.1] = 0
    
    if data2_max - data2_min < 3:
        normalized_array_2[:] = 0
    else:
        normalized_array_2 = (data2 - data_min) / (data_max - data_min)

        # 閾値以下の値を0にする
        normalized_array_2[normalized_array_2 <= 0.1] = 0


    return normalized_array_1, normalized_array_2 

def convert_to_fft_data_upper(path:str):
    average_strengths_1 = []
    average_strengths_2 = []
    try:
        raw_samples_list = np.load(path, allow_pickle=True)

        key = path.split('_')[1]
        if key == '193':
            key = '1930'

        frequncy = int(key) * 1e6

        for samples in raw_samples_list:
            spectrum = np.fft.fftshift(np.fft.fft(samples))
            fft_vals = 20 * np.log10(np.abs(spectrum))


            freqs = np.fft.fftshift(np.fft.fftfreq(int(sample_rate*0.01), 1/sample_rate)) + frequncy
            index_upper_0 = np.where(freqs > frequncy + 0.50e6)[0][0]
            index_upper_1 = np.where(freqs < frequncy + 2.25e6)[0][-1]

            index_upper_2 = np.where(freqs > frequncy + 2.25e6)[0][0]
            index_upper_3 = np.where(freqs < frequncy + 5.00e6)[0][-1]

            average_strength_1 = np.mean(fft_vals[index_upper_0:index_upper_1])
            average_strength_2 = np.mean(fft_vals[index_upper_2:index_upper_3])
            average_strengths_1.append(average_strength_1)
            average_strengths_2.append(average_strength_2)

        return average_strengths_1,average_strengths_2
    except KeyboardInterrupt:
        # キーボード割り込みが発生した場合には、メッセージを表示してプログラムを終了します
        print("Program interrupted by user.")
        sys.exit()

    except Exception as e:
        # 他の例外が発生した場合には、その内容を表示します
        print(f"An error occurred: {e}")
        return average_strengths_1,average_strengths_2
    
def convert_to_fft_data_lower(path:str):
    average_strengths_1 = []
    average_strengths_2 = []

    try:
        raw_samples_list = np.load(path, allow_pickle=True)

        key = path.split('_')[1] 
        frequncy = int(key) * 1e6


        for samples in raw_samples_list:
            spectrum = np.fft.fftshift(np.fft.fft(samples))
            fft_vals = 20 * np.log10(np.abs(spectrum))


            freqs = np.fft.fftshift(np.fft.fftfreq(int(sample_rate*0.01), 1/sample_rate)) + frequncy

            index_lower_0 = np.where(freqs > frequncy - 2.25e6)[0][0]
            index_lower_1 = np.where(freqs < frequncy - 0.55e6)[0][-1]
            index_lower_2 = np.where(freqs > frequncy - 5.00e6)[0][0]
            index_lower_3 = np.where(freqs < frequncy - 2.25e6)[0][-1]

            average_strength_1 = np.mean(fft_vals[index_lower_0:index_lower_1])
            average_strength_2 = np.mean(fft_vals[index_lower_2:index_lower_3])

            average_strengths_1.append(average_strength_1)
            average_strengths_2.append(average_strength_2)

        return average_strengths_1,average_strengths_2
    except KeyboardInterrupt:
        # キーボード割り込みが発生した場合には、メッセージを表示してプログラムを終了します
        print("Program interrupted by user.")
        sys.exit()

    except Exception as e:
        # 他の例外が発生した場合には、その内容を表示します
        print(f"An error occurred: {e}")
        return average_strengths_1,average_strengths_2

# for Linux
# directory_path = '/media/makun/prod/' 

# for Mac   
directory_path = '/Volumes/volume/1114/'


for file_name_1,file_name_2,frequency_width,filename in plot_far_file_path:

    data1_1,data1_2 = convert_to_fft_data_upper(directory_path + file_name_1)
    plot_data_1,_ = normalize(data1_1,data1_2)
    data2_1,data2_2 = convert_to_fft_data_upper(directory_path + file_name_2)
    plot_data_2,_ = normalize(data2_1,data2_2)

    corr = max_shifted_correlation(plot_data_1, plot_data_2)
    dtw = dtw_distance(plot_data_1, plot_data_2)

    # corrとdtwを小数点第３位を四捨五入して表示
    corr = round(corr[0], 3)
    dtw = round(dtw, 3)

    plt.figure()

    # data1_1とdata2_1をプロット
    plt.plot(plot_data_1, lw=1 ,label='機器1')
    plt.plot(plot_data_2, lw=1 ,label='機器2')

    for i in plot_data_1:
        if i < 0:
            print(i)
    for i in plot_data_2:
        if i < 0:
            print(i)
    # タイトルと凡例を追加
    # plt.title(f"時間ごとの電波強度の変化({frequency_width}) \n 相関係数:{corr}, DTW距離:{dtw}")
    # plt.text(x=max(plt.xlim())*0.05, y=max(plt.ylim())*0.85, s=f"相関係数: {corr}", 
    #         fontsize=12, fontweight='bold', color='black', 
    #         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    # plt.legend(fontsize=12)

    # x軸とy軸のラベルを追加
    plt.xlabel("時間(秒)",fontsize=18,fontweight='bold')
    plt.ylabel("電波強度",fontsize=18,fontweight='bold')

    x_ticks = np.linspace(0, len(data1_1), 6)  # 0からデータの長さまで6個の点を生成
    x_labels = [0, 6, 12, 18, 24, 30]  # 目盛りのラベル
    plt.xticks(x_ticks, x_labels)

    # x軸とy軸の範囲を設定 (必要に応じて調整してください)
    plt.xlim([0, len(data1_1)])  # 例えば、データポイント数に合わせて調整
    plt.ylim(min(min(plot_data_1),min(plot_data_2)), max(max(plot_data_1), max(plot_data_2)))  # 最小値と最大値を基に範囲を設定

    # ファイルに保存
    plt.savefig('./fig/' + filename + '.pdf')
