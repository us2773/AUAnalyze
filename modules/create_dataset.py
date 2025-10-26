import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from modules.models import Base, main_table, au_table
from modules import  au_map, db_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import between
from datetime import datetime
from zoneinfo import ZoneInfo

# 日付は範囲指定

resultdir =  "result"

def create_dataset(date_start: str, date_end: str, person_list: list) :

    format = "%Y%m%d-%H:%M:%S"
    start_time = datetime.strptime(date_start + "-00:00:00", format).replace(tzinfo=ZoneInfo("Asia/Tokyo"))
    end_time = datetime.strptime(date_end + "-23:59:59", format).replace(tzinfo=ZoneInfo("Asia/Tokyo"))

    all_data = []

    with Session(db_engine.engine) as session: 
        stmt_main = select(main_table).where(main_table.person.in_(person_list)).filter(between(main_table.date, start_time, end_time))
        all_data = session.scalars(stmt_main).all()
        
        columns = ["date", "person",
                    "AU01_mean", "AU02_mean", "AU04_mean", "AU05_mean","AU06_mean","AU07_mean","AU09_mean","AU10_mean","AU12_mean","AU14_mean","AU15_mean","AU17_mean","AU20_mean","AU23_mean","AU25_mean","AU26_mean","AU45_mean", 
                    "AU01_var", "AU02_var", "AU04_var", "AU05_var","AU06_var","AU07_var","AU09_var","AU10_var","AU12_var","AU14_var","AU15_var","AU17_var","AU20_var","AU23_var","AU25_var","AU26_var","AU45_var",
                    "AU01_var", "AU02_peakfreq", "AU04_peakfreq", "AU05_peakfreq","AU06_peakfreq","AU07_peakfreq","AU09_peakfreq","AU10_peakfreq","AU12_peakfreq","AU14_peakfreq","AU15_peakfreq","AU17_peakfreq","AU20_peakfreq","AU23_peakfreq","AU25_peakfreq","AU26_peakfreq","AU45_peakfreq", 
                    "vas_sleepiness","vas_annoyed","vas_painful"]
        #print(len(columns))
        df = pd.DataFrame(columns=columns)
        
        for main_data in all_data:
            stmt_au = select(au_table).where(au_table.data_id == main_data.id)
            au_data = session.scalars(stmt_au).one()
            
            record_list = [str(main_data.date), main_data.person] + au_data.trend_mean + au_data.trend_var + au_data.peak_freq + main_data.fatigue_level
            #print(len(record_list))
            df_append = pd.DataFrame(data=[record_list], columns=columns)
            # print(df_append.head())
            #print(df_append)
            df = pd.concat([df, df_append], ignore_index=True, axis=0)
        
        print(df.head())
        print(df.shape)
        df.to_csv(f"{resultdir}/AUAnalyze_dataset_{date_start}_{date_end}.csv",encoding='utf-8_sig')