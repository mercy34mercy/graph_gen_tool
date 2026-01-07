import subprocess
import pandas as pd
import numpy as np
from datetime import datetime
import threading
import argparse
import folium
from folium.plugins import HeatMap
import webbrowser
import os
import time
import serial
import pynmea2
import csv

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description='Wi-Fi Signal Strength Mapper')
parser.add_argument('--ssid', type=str, help='SSID of the Wi-Fi network to monitor')
parser.add_argument('--port', type=str, default='/dev/ttyUSB0', help='GPS module serial port (e.g., /dev/ttyUSB0)')
parser.add_argument('--baudrate', type=int, default=115200, help='Baud rate for GPS module communication')
args = parser.parse_args()

selected_ssid = args.ssid
gps_port = args.port
gps_baudrate = args.baudrate

csv_file = 'wifi_gps_data.csv'
data_lock = threading.Lock()  # データアクセス時のロック

# CSVファイルの初期化（ヘッダーを書き込む）
def initialize_csv():
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'latitude', 'longitude', 'ssid', 'signal_strength'])

initialize_csv()

def get_gps_data():
    # ポートとボーレートを設定
    try:
        gps_serial = serial.Serial(gps_port, gps_baudrate, timeout=1)
    except serial.SerialException as e:
        print(f"GPSモジュールに接続できませんでした: {e}")
        return None, None

    last_valid_data_received = time.time()  # 有効なデータを最後に受信した時刻

    try:
        while True:
            line = gps_serial.readline().decode('ascii', errors='replace').strip()
            if line.startswith('$GNGGA') or line.startswith('$GNRMC') or line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                try:
                    msg = pynmea2.parse(line)
                    lat = msg.latitude
                    lon = msg.longitude

                    if lat != 0.0 and lon != 0.0:
                        return lat, lon

                    # 3秒以上新しい有効なデータがない場合
                    if time.time() - last_valid_data_received > 3:
                        print("3秒間有効なGPSデータがありません。")
                        return None, None

                except pynmea2.ParseError:
                    continue
    except serial.SerialException as e:
        print(f"シリアル通信エラー: {e}")
        return None, None
    except KeyboardInterrupt:
        gps_serial.close()
        return None, None

def get_wifi_data():
    # 周囲のWi-Fiアクセスポイントをスキャン
    result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
    networks = result.stdout

    ssid_list = []
    signal_list = []

    # スキャン結果を分割してパース
    cells = networks.split('Cell ')
    for cell in cells[1:]:
        try:
            # 各セルの情報を取得
            lines = cell.split('\n')
            ssid = None
            signal = None

            for line in lines:
                line = line.strip()
                if "ESSID:" in line:
                    ssid = line.split('ESSID:')[1].strip('"')
                elif "Signal level=" in line:
                    signal_part = line.split('Signal level=')[1]
                    signal_value = signal_part.split(' ')[0]
                    signal_value = signal_value.replace('dBm', '').strip()
                    try:
                        signal = int(signal_value)
                    except ValueError:
                        signal = -100  # 取得できなかった場合のデフォルト値

            if ssid is not None and signal is not None:
                ssid_list.append(ssid)
                signal_list.append(signal)
        except Exception as e:
            continue

    # 電波強度が最も強いSSIDを選択
    if ssid_list and signal_list:
        networks = []
        for ssid, signal in zip(ssid_list, signal_list):
            networks.append({'ssid': ssid, 'signal': signal})

        # ユーザーがSSIDを指定していない場合、強い順にリストを表示
        global selected_ssid
        if selected_ssid is None:
            networks_sorted = sorted(networks, key=lambda x: x['signal'], reverse=True)
            print("検出されたSSID一覧:")
            for idx, network in enumerate(networks_sorted):
                print(f"{idx + 1}. SSID: {network['ssid']}, Signal: {network['signal']} dBm")
            try:
                ssid_index = int(input("測定するSSIDの番号を選択してください: ")) - 1
                selected_network = networks_sorted[ssid_index]
                selected_ssid = selected_network['ssid']
                return selected_network['ssid'], selected_network['signal']
            except (IndexError, ValueError):
                print("正しい番号を入力してください。")
                return None, None
        else:
            for network in networks:
                if network['ssid'] == selected_ssid:
                    return network['ssid'], network['signal']
            # 指定したSSIDが見つからない場合
            print(f"指定したSSID '{selected_ssid}' が見つかりませんでした。")
            return None, None
    else:
        print("Wi-Fiネットワークが見つかりませんでした。")
        return None, None

def collect_data():
    global selected_ssid
    while True:
        # GPSデータ取得
        lat_lon = get_gps_data()
        if lat_lon is None or None in lat_lon:
            continue
        else:
            lat, lon = lat_lon

        # Wi-Fiデータ取得
        ssid, signal = get_wifi_data()

        # SSIDが取得できない場合はスキップ
        if ssid is None or signal is None:
            continue

        # データの追加
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = [current_time, lat, lon, ssid, signal]

        # CSVに書き込み（ロックを使用）
        with data_lock:
            with open(csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)

        time.sleep(3)  # 3秒間隔でデータ収集

def generate_map():
    global selected_ssid
    map_file = 'wifi_signal_map.html'
    # 地図の初期化
    m = folium.Map(zoom_start=15)
    first_run = True

    while True:
        # データの取得（ロックを使用）
        with data_lock:
            if not os.path.exists(csv_file):
                time.sleep(10)
                continue
            df = pd.read_csv(csv_file)

        # 指定したSSIDのデータをフィルタリング
        df_ssid = df[df['ssid'] == selected_ssid]

        if not df_ssid.empty:
            # 地図のクリア
            last_lat = df_ssid.iloc[-1]['latitude']
            last_lon = df_ssid.iloc[-1]['longitude']
            m = folium.Map(location=[last_lat, last_lon], zoom_start=15)
            heat_data = df_ssid[['latitude', 'longitude', 'signal_strength']].values.tolist()
            HeatMap(heat_data, max_zoom=18, radius=15).add_to(m)

            # 地図の保存
            m.save(map_file)

            # 初回のみブラウザを開く
            if first_run:
                webbrowser.open('file://' + os.path.realpath(map_file))
                first_run = False

        time.sleep(10)  # 10秒間隔で地図を更新

# データ収集スレッドの開始
data_thread = threading.Thread(target=collect_data)
data_thread.daemon = True
data_thread.start()

# 地図生成スレッドの開始
map_thread = threading.Thread(target=generate_map)
map_thread.daemon = True
map_thread.start()

# メインスレッドの維持
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("プログラムを終了します。")
    # スレッド内で特別なクリーンアップは不要
    pass