from PyOpenFace import *
from get_AUdata import *
import data_regiseter

outputdir = "output"

# Input内の動画ファイル名取得(拡張子なし)
input_movies = get_movie_file()
print(input_movies)

# movie to CSV
# get_OpenFace_result()
#transfer_input_movies() # デバッグ時はコメントアウト

df_list = []

for file in input_movies :
    csv_file = f"{outputdir}/{file}.csv"
    df = csv_to_dataframe(csv_file)
    df_list.append(df)

data_regiseter.register(input_movies)