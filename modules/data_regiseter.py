import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  

from sqlalchemy import select
from sqlalchemy.orm import Session
from modules import get_AUdata, data_regiseter, collected_data, PyOpenFace
from modules.models import Base, main_table, au_table
from datetime import datetime
from zoneinfo import ZoneInfo
from modules import db_engine
import json
import glob

outputdir = "output"
jsondir = "json"

def register(all_data: list) :
    # collected_data型格納リスト
    # Table 作成
    Base.metadata.create_all(db_engine.engine)
    
    with Session(db_engine.engine) as session:
        print(len(all_data))
        for data in all_data :
            print(data.get_movie_name())
            movie_name = data.get_movie_name()
            # メタデータ登録
            format = "%Y%m%d%H%M%S"
            
            person = data.get_user_name()
            date = data.get_date()
            fatigue_level = data.get_vas_list()
            
            capture_time = datetime.strptime(date, format).replace(tzinfo=ZoneInfo("Asia/Tokyo"))
            
            stmt = select(main_table).where(main_table.movie_name == movie_name)
            old_data = session.scalars(stmt).first()
            if old_data == None :
                main_data = main_table(
                    movie_name = movie_name,
                    date = capture_time,
                    registed_date =datetime.now(),
                    fatigue_level = fatigue_level,
                    person = person
                )
                session.add(main_data)
            else :
                print(f"movie:{movie_name} is already registed")
        session.commit()

def json_analyze() :
    # JSONファイルをすべて取得
    jsons = glob.glob(jsondir+"/*.json")
    print(jsons)
    
    all_data = []
    
    for json_file in jsons:
    # 辞書型リストに変換
        with open(json_file, "r", encoding="utf-8") as f :
            json_list  = json.load(f) # アプリが出力するJSONはトップレベルが配列
            for data in json_list :
                all_data.append(data)
            
    return all_data

def get_collected_data_list() :
    input_movies = PyOpenFace.get_movie_file()
    print(f"input movies: {input_movies}")
    
    # JSON解析
    data_dicts = data_regiseter.json_analyze()
    all_data = []
    for dict in data_dicts :
        # 拡張子の除去
        movie_name = os.path.splitext(os.path.basename(dict["movie_name"]))[0]
        if movie_name in input_movies :
            data = collected_data.collected_data(dict["userID"], movie_name, dict["date"], [dict["vas_sleepiness"], dict["vas_annoyed"], dict["vas_painful"]])
            all_data.append(data)
        else :
            print(f"{dict["movie_name"]} is not exest.")
    
    return all_data

def au_register(all_data: list) :
    # AU_table登録
    with Session(db_engine.engine) as session:
        for data in all_data :
            # mainデータ取得
            stmt = select(main_table).where(main_table.movie_name == data.get_movie_name())
            main_data = session.scalars(stmt).one()
            print(f"id: {main_data.id}")
            
            stmt_exest = select(au_table).where(au_table.data_id == main_data.id)
            old_data = session.scalars(stmt_exest).first()
            if old_data == None :
                # 統計分析
                csv_file = f"{outputdir}/{data.get_movie_name()}.csv"
                df = get_AUdata.csv_to_dataframe(csv_file)
                
                result_trend_noise = get_AUdata.get_trend_noise(df)
                result_peak = get_AUdata.get_AU_peak(df)
                
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
            else :
                print(f"this data '{main_data.id}' is already registed.")
        session.commit()
