import glob
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.signal import find_peaks

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
def AU_trend_noise(df: pd.DataFrame):
    
    lst_AUR_moving_mean = []
    lst_AUR_moving_var = []
    lst_AUR_residual_mean = []
    lst_AUR_residual_var = []
    
    for plot_num in range(17) :
        AUR_start = df.columns.get_loc(" AU01_r")
        AUR_moving = df.iloc[:, AUR_start + plot_num]
        AUR_name = df.columns[AUR_start + plot_num]

        # LOWESSによるトレンド抽出
        trend_est = lowess(AUR_moving, df[" timestamp"], frac=0.1, return_sorted=False)

        # 残差計算
        residual = AUR_moving - trend_est
        df[f"{AUR_name}_trend"] = trend_est
        df[f"{AUR_name}_fluct"] = residual

        # 統計情報
        AUR_moving_mean = float(AUR_moving.mean())
        AUR_moving_var = float(AUR_moving.var())
        AUR_residual_mean = float(residual.mean())
        AUR_residual_var = float(residual.var())
        
        lst_AUR_moving_mean.append(AUR_moving_mean)
        lst_AUR_moving_var.append(AUR_moving_var)
        lst_AUR_residual_mean.append(AUR_residual_mean)
        lst_AUR_residual_var.append(AUR_residual_var)

    result_dict = {"AUR_moving_mean": lst_AUR_moving_mean, "AUR_moving_var": lst_AUR_moving_var,"AUR_residual_mean": lst_AUR_residual_mean, "AUR_residual_var": lst_AUR_residual_var}
    print(result_dict)
    return result_dict

# ピーク検出
def get_AU_peak(df: pd.DataFrame):
    lst_num = []
    lst_f = []
    for plot_num in range(17):
        au_col = df.columns.get_loc(" AU01_r") + plot_num
        signal = df.iloc[:, au_col].values
        times = df[" timestamp"].values

        peaks, _ = find_peaks(signal, height=0.1, distance=5, prominence=0.1)

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

if __name__ == "__main__" :
    list = []
    # 統計分析前のDataFrameを適当なリストに格納
    # トレンド抽出、ピーク検出を実行しSQLに登録する処理を後で実装
    for i in range(5) :
        df = csv_to_dataframe(outputs[i])
        list.append(df)
    print(len(list))
    AU_trend_noise(list[0])
    get_AU_peak(list[0])