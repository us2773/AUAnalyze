from PyOpenFace import *
from get_AUdata import *
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, main_table, au_table
import data_regiseter
import db_config

outputdir = "output"

# Input内の動画ファイル名取得(拡張子なし)
input_movies = get_movie_file()
print(input_movies)

# movie to CSV
get_OpenFace_result()
#transfer_input_movies() # デバッグ時はコメントアウト

data_regiseter.register(input_movies)

# Engine作成
engine = create_engine(f"postgresql+psycopg2://{db_config.user_name}:{db_config.password}@{db_config.host_name}/facehealthdb",echo=True)

with Session(engine) as session:
    for movie_name in input_movies :
        stmt = select(main_table).where(main_table.movie_name == movie_name)
        main_data = session.scalars(stmt).one()
        print(f"id: {main_data.id}")
        
        # 統計分析
        csv_file = f"{outputdir}/{movie_name}.csv"
        df = csv_to_dataframe(csv_file)
        
        result_trend_noise = AU_trend_noise(df)
        result_peak = get_AU_peak(df)
        
        # AU_table登録
        au_data = au_table(
            data_id = main_data.id,
            trend_mean = result_trend_noise["AUR_moving_mean"],
            trend_var = result_trend_noise["AUR_moving_var"],
            noise_mean = result_trend_noise["AUR_residual_mean"],
            noise_var = result_trend_noise["AUR_residual_var"],
            num_of_peak =result_peak["num"],
            peak_freq = result_peak["freq"],
        )
        session.add(au_data)
    session.commit()