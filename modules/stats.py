from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import between
from models import Base, main_table, au_table
from datetime import datetime
from zoneinfo import ZoneInfo
import db_config

engine = create_engine(f"postgresql+psycopg2://{db_config.user_name}:{db_config.password}@{db_config.host_name}/facehealthdb",echo=True)

def get_stats(person: str, date: str, num: int) :
    format = "%Y%m%d-%H:%M:%S"
    start_time = datetime.strptime(date + "-00:00:00", format).replace(tzinfo=ZoneInfo("Asia/Tokyo"))
    end_time = datetime.strptime(date + "-23:59:59", format).replace(tzinfo=ZoneInfo("Asia/Tokyo"))
    print(start_time)
    with Session(engine) as session: 
        # 日付は範囲指定
        stmt = select(main_table).where(main_table.person==person).filter(between(main_table.date, start_time, end_time))
        data = session.scalars(stmt).all()
        
        if num == 0:
            # 全データ
            for i in range(len(data)) :
                print(data[i].person)
                print(data[i].id)
                print(data[i].date)
        
        else :
            print(data[num-1].person)
            print(data[num-1].id)

if __name__ == "__main__" :
    get_stats("guest", "20250901",0)