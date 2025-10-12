import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # modules の親を追加

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from modules.models import Base, main_table, au_table
from datetime import datetime
from zoneinfo import ZoneInfo
from modules import db_config

def register(movie_list: list) :
    # Engine作成
    # mainに移動？
    engine = create_engine(f"postgresql+psycopg2://{db_config.user_name}:{db_config.password}@{db_config.host_name}/facehealthdb",echo=True)
    # Table 作成
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        for i in range(len(movie_list)) :
            movie_name = movie_list[i]
            # メタデータ登録
            # 動画撮影アプリ完成後はJSON解析による自動入力
            format = "%Y%m%d%H%M%S"
            
            person = input("what is your name?:")
            date = input(f"what is the day you capture the movie {movie_list[i]}(yyyymmddHHmmSS)?: ")
            
            capture_time = datetime.strptime(date, format).replace(tzinfo=ZoneInfo("Asia/Tokyo"))
            
            stmt = select(main_table).where(main_table.movie_name == movie_name)
            data = session.scalars(stmt).first()
            if data == None :
                main_data = main_table(
                    movie_name = movie_name,
                    date = capture_time,
                    registed_date =datetime.now(),
                    person = person
                )
                session.add(main_data)
        session.commit()
