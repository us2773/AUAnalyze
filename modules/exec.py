from PyOpenFace import *
from get_AUdata import *
import data_regiseter

outputdir = "output"

# Input内の動画ファイル名取得
input_movies = get_movie_file()

# movie to CSV
get_OpenFace_result()
#transfer_input_movies() # デバッグ時はコメントアウト

list = []

for file in input_movies :
    csv_file = f"{outputdir}/{file}.csv"
    df = csv_to_dataframe(csv_file)
    list.append(df)

data_regiseter.register()