import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
import pandas as pd

# データの読み込み
df = pd.read_csv('./test.csv')

# デバイス名を改行して横幅を制限
def format_device_name(name):
    if 'Jetson Orin Nano' in name:
        return name.replace('Jetson Orin Nano', 'Jetson Orin Nano\n')
    return name

def create_graph(df, filename_suffix=''):
    # デバイス名と各時間を取得
    devices = df['デバイス'].values
    witness_times = df['Witness生成(秒)'].values
    proof_times = df['Proof生成(秒)'].values

    devices_formatted = [format_device_name(d) for d in devices]

    # 積み上げ棒グラフのプロット
    fig, ax = plt.subplots(figsize=(14, 7))

    x = np.arange(len(devices_formatted))
    width = 0.6

    # 積み上げ棒グラフ
    bars1 = ax.bar(x, witness_times, width, label='Witness生成', color='#4CAF50', edgecolor='black')
    bars2 = ax.bar(x, proof_times, width, bottom=witness_times, label='Proof生成', color='#FF9800', edgecolor='black')

    # 各セグメントに数値を表示
    for i, (w, p) in enumerate(zip(witness_times, proof_times)):
        total = w + p
        # Witness部分（中央に表示、十分な高さがある場合のみ）
        if w > 0.3:
            ax.text(i, w/2, f'{w:.3f}', ha='center', va='center', fontsize=18, fontweight='bold', color='white')
        # Proof部分（中央に表示、十分な高さがある場合のみ）
        if p > 0.3:
            ax.text(i, w + p/2, f'{p:.3f}', ha='center', va='center', fontsize=18, fontweight='bold', color='white')
        # 合計を上に表示
        ax.text(i, total + 0.12, f'{total:.3f}秒', ha='center', va='bottom', fontsize=20, fontweight='bold')

    # X軸の設定
    ax.set_xticks(x)
    ax.set_xticklabels(devices_formatted)

    # 軸ラベルとフォントサイズ設定
    ax.set_xlabel('デバイス', fontsize=24, fontweight='bold')
    ax.set_ylabel('計算時間(秒)', fontsize=24, fontweight='bold')
    ax.tick_params(axis='both', labelsize=20)
    ax.set_ylim(0, max(witness_times + proof_times) * 1.15)

    # タイトル
    ax.set_title('rapidsnark', fontsize=28, fontweight='bold')

    # 凡例
    ax.legend(fontsize=18, loc='upper right')

    # グリッドを追加
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # プロットの保存
    plt.tight_layout()
    plt.savefig(f'./fig/benchmark{filename_suffix}.pdf')
    plt.savefig(f'./fig/benchmark{filename_suffix}.png')
    plt.close()
    print(f'グラフを保存しました: ./fig/benchmark{filename_suffix}.pdf, ./fig/benchmark{filename_suffix}.png')

def create_proof_only_graph(df, filename_suffix=''):
    # デバイス名と各時間を取得
    devices = df['デバイス'].values
    proof_times = df['Proof生成(秒)'].values

    devices_formatted = [format_device_name(d) for d in devices]

    # 棒グラフのプロット
    fig, ax = plt.subplots(figsize=(14, 7))

    x = np.arange(len(devices_formatted))
    width = 0.6

    # 棒グラフ
    bars = ax.bar(x, proof_times, width, label='Proof生成', color='#FF9800', edgecolor='black')

    # 各バーに数値を表示
    for i, p in enumerate(proof_times):
        ax.text(i, p + 0.003, f'{p:.3f}秒', ha='center', va='bottom', fontsize=20, fontweight='bold')

    # X軸の設定
    ax.set_xticks(x)
    ax.set_xticklabels(devices_formatted)

    # 軸ラベルとフォントサイズ設定
    ax.set_xlabel('デバイス', fontsize=24, fontweight='bold')
    ax.set_ylabel('計算時間(秒)', fontsize=24, fontweight='bold')
    ax.tick_params(axis='both', labelsize=20)
    ax.set_ylim(0, max(proof_times) * 1.25)

    # タイトル
    ax.set_title('rapidsnark (Proof生成のみ)', fontsize=28, fontweight='bold')

    # グリッドを追加
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # プロットの保存
    plt.tight_layout()
    plt.savefig(f'./fig/proof_only{filename_suffix}.pdf')
    plt.savefig(f'./fig/proof_only{filename_suffix}.png')
    plt.close()
    print(f'グラフを保存しました: ./fig/proof_only{filename_suffix}.pdf, ./fig/proof_only{filename_suffix}.png')

def create_mac_comparison_graph(df):
    # MacとMac Dockerのデータを抽出
    df_mac = df[df['デバイス'].isin(['MacBook Pro', 'Mac Docker'])]

    devices = df_mac['デバイス'].values
    witness_times = df_mac['Witness生成(秒)'].values
    proof_times = df_mac['Proof生成(秒)'].values

    # 積み上げ棒グラフのプロット
    fig, ax = plt.subplots(figsize=(10, 7))

    x = np.arange(len(devices))
    width = 0.5

    # 積み上げ棒グラフ
    bars1 = ax.bar(x, witness_times, width, label='Witness生成', color='#4CAF50', edgecolor='black')
    bars2 = ax.bar(x, proof_times, width, bottom=witness_times, label='Proof生成', color='#FF9800', edgecolor='black')

    # 各セグメントに数値を表示
    for i, (w, p) in enumerate(zip(witness_times, proof_times)):
        total = w + p
        # Witness部分
        if w > 0.15:
            ax.text(i, w/2, f'{w:.3f}', ha='center', va='center', fontsize=18, fontweight='bold', color='white')
        # Proof部分
        if p > 0.05:
            ax.text(i, w + p/2, f'{p:.3f}', ha='center', va='center', fontsize=18, fontweight='bold', color='white')
        # 合計を上に表示
        ax.text(i, total + 0.02, f'{total:.3f}秒', ha='center', va='bottom', fontsize=20, fontweight='bold')

    # X軸の設定
    ax.set_xticks(x)
    ax.set_xticklabels(devices)

    # 軸ラベルとフォントサイズ設定
    ax.set_xlabel('デバイス', fontsize=24, fontweight='bold')
    ax.set_ylabel('計算時間(秒)', fontsize=24, fontweight='bold')
    ax.tick_params(axis='both', labelsize=20)
    ax.set_ylim(0, max(witness_times + proof_times) * 1.2)

    # タイトル
    ax.set_title('rapidsnark (Mac vs Mac Docker)', fontsize=28, fontweight='bold')

    # 凡例
    ax.legend(fontsize=18, loc='upper right')

    # グリッドを追加
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # プロットの保存
    plt.tight_layout()
    plt.savefig('./fig/mac_comparison.pdf')
    plt.savefig('./fig/mac_comparison.png')
    plt.close()
    print('グラフを保存しました: ./fig/mac_comparison.pdf, ./fig/mac_comparison.png')

# WSLありのグラフ
create_graph(df, '')
create_proof_only_graph(df, '')

# WSLなしのグラフ
df_no_wsl = df[~df['デバイス'].isin(['WSL', 'Mac Docker'])]
create_graph(df_no_wsl, '_no_wsl')
create_proof_only_graph(df_no_wsl, '_no_wsl')

# Mac比較グラフ
create_mac_comparison_graph(df)
