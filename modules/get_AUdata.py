import glob
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

outputdir = "output"
outputs = glob.glob(outputdir+"/*")
print(outputs)

# CSVをクレンジングしDataFrameを取得
# 直近で動画→CSV処理をした動画のみ行うように後で変更
def csv_to_dataframe(file_name) :
    try:
        print(file_name)
        df = pd.read_csv(file_name)
        df = df[(df[" success"] == 0) | (df[" success"] == 1)]
        return df
    except Exception as e:
        raise RuntimeError(f"fail to load csv: {e}")
    
# AUをノイズとトレンドに分離
def get_trend_noise(df: pd.DataFrame):
    
    lst_AUR_moving_mean = []
    lst_AUR_moving_var = []
    lst_AUR_residual_mean = []
    lst_AUR_residual_var = []
    
    # AU種数分だけループ
    for plot_num in range(17) :
        trend_est, residual = separate_AU_trend_noise(df, plot_num)

        # 統計情報
        AUR_moving_mean = float(trend_est.mean())
        AUR_moving_var = float(trend_est.var())
        AUR_residual_mean = float(residual.mean())
        AUR_residual_var = float(residual.var())
        
        lst_AUR_moving_mean.append(AUR_moving_mean)
        lst_AUR_moving_var.append(AUR_moving_var)
        lst_AUR_residual_mean.append(AUR_residual_mean)
        lst_AUR_residual_var.append(AUR_residual_var)

    result_dict = {"AUR_moving_mean": lst_AUR_moving_mean, "AUR_moving_var": lst_AUR_moving_var,"AUR_residual_mean": lst_AUR_residual_mean, "AUR_residual_var": lst_AUR_residual_var}
    print(result_dict)
    return result_dict

def separate_AU_trend_noise(df, plot_num) :
    AUR_start = df.columns.get_loc(" AU01_r")
    AUR_row = df.iloc[:, AUR_start + plot_num]
    AUR_name = df.columns[AUR_start + plot_num]
        
    # LOWESSによるトレンド抽出
    trend_est = lowess(AUR_row, df[" timestamp"], frac=0.1, return_sorted=False)

    # 以降の処理を関数で実装
    # 引数はAUR_Moving, residual, trend_est
    
    # グラフ出力関数も実装
    
    # 残差計算
    residual = AUR_row - trend_est
    df[f"{AUR_name}_trend"] = trend_est
    df[f"{AUR_name}_fluct"] = residual
    return (trend_est, residual)

def show_trend_noise_graph(df, plot_num) :
    AUR_start = df.columns.get_loc(" AU01_r")
    AUR_row = df.iloc[:, AUR_start + plot_num]
    AUR_name = df.columns[AUR_start + plot_num]
    
    trend_est, residual = separate_AU_trend_noise(df, plot_num)
    # グラフ描画
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(df[" timestamp"], AUR_row, label="Original", color = "gray")
    ax.plot(df[" timestamp"], trend_est, label="Trend (LOWESS)", color="blue")
    ax.plot(df[" timestamp"], residual, label="Residual (Fluctuation)", color="red", linestyle="--")
    ax.legend()
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(AUR_name)
    ax.set_title(f"{AUR_name}: Trend and Fluctuation")
    fig.tight_layout()
    plt.show()
    
    return fig

# ピーク検出
def get_AU_peak(df: pd.DataFrame):
    lst_num = []
    lst_f = []
    for plot_num in range(17):
        peaks, times = find_AU_peaks(df, plot_num)
        # グラフ出力関数も実装

        num = len(peaks)
        print(num)
        if num == 0 :
            f = 0
        else :
            f = float(times[-1] / num)
        
        lst_num.append(num)
        lst_f.append(f)
        
    result_dict = {"num": lst_num, "freq": lst_f}
    return result_dict

def find_AU_peaks(df, plot_num) :
    au_col = df.columns.get_loc(" AU01_r") + plot_num
    signal = df.iloc[:, au_col].values
    times = df[" timestamp"].values

    peaks, _ = find_peaks(signal, height=0.1, distance=5, prominence=0.1)
    return peaks, times

def show_AU_peak_graph(df, plot_num) :
    peaks, times = find_AU_peaks(df, plot_num)
    au_col = df.columns.get_loc(" AU01_r") + plot_num
    signal = df.iloc[:, au_col].values
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.plot(times, signal, label="Original")
    ax.scatter(times[peaks], signal[peaks], color='red', label='Expression Peaks')
    ax.set_title(f"{df.columns[au_col]}: transition")
    ax.set_xlabel("Timestamp (s)")
    ax.set_ylabel("AU Strength")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    plt.show()
    
    return fig


if __name__ == "__main__" :
    list = []
    # 統計分析前のDataFrameを適当なリストに格納
    # トレンド抽出、ピーク検出を実行しSQLに登録する処理を後で実装
    df = csv_to_dataframe(outputs[1])
    fig = show_AU_peak_graph(df, 1)
    list.append(df)
    print(len(list))
    