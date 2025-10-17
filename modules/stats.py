import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # modules の親を追加

from modules.models import Base, main_table, au_table
from modules import  au_map, db_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import between
from datetime import datetime
from zoneinfo import ZoneInfo

def get_data_from_property(person: str, date: str) :
    # 日付は範囲指定
    format = "%Y%m%d-%H:%M:%S"
    start_time = datetime.strptime(date + "-00:00:00", format).replace(tzinfo=ZoneInfo("Asia/Tokyo"))
    end_time = datetime.strptime(date + "-23:59:59", format).replace(tzinfo=ZoneInfo("Asia/Tokyo"))
    print(start_time)
    with Session(db_engine.engine) as session: 
        stmt = select(main_table).where(main_table.person==person).filter(between(main_table.date, start_time, end_time))
        return session.scalars(stmt).all()

def get_stats(person: str, date: str, num: int, au: int) :
    # 日付は範囲指定
    data = get_data_from_property(person, date, num, au)
        
    if num == 0:
        # 全データ
        for i in range(len(data)) :
            print(type(data[i].id))
            au_data = query_au_table(data[i].id)
            print(f"{data[i].person}/{data[i].date}/{num}")
            if au == 0 :
                for i in range(17) :
                    show_stats(au_data, i)
            else :
                show_stats(au_data, au)
            
    else :
        print(data[num-1].person)
        print(data[num-1].id)
        if au == 0 :
                for i in range(17) :
                    show_stats(au_data, i)
        else :
            show_stats(au_data, au)
            
def query_au_table(id) :
    with Session(db_engine.engine) as session :
        stmt = select(au_table).where(au_table.data_id == id)
        data = session.scalars(stmt).first()
        return data
    
def show_stats(au_data: au_table, au: int) :
    print(f"{au_map.au_map[au]}")
    print(f"AUR moving mean = {au_data.trend_mean[au]}")
    print(f"AUR moving var = {au_data.trend_mean[au]}")
    print(f"AUR residual mean = {au_data.trend_mean[au]}")
    print(f"AUR residual var = {au_data.trend_mean[au]}")
    print(f"num of peak = {au_data.trend_mean[au]}")
    print(f"peak freqency = {au_data.trend_mean[au]}")
    print()


if __name__ == "__main__" :
    get_stats("guest", "20250901",0, 0)