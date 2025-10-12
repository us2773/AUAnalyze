from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, main_table, au_table
from datetime import datetime
import db_config

def register(movie_list: list) :
    # Engine作成
    # mainに移動？
    engine = create_engine(f"postgresql+psycopg2://{db_config.user_name}:{db_config.password}@{db_config.host_name}/facehealthdb",echo=True)
    # Table 作成
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        for i in range(len(movie_list)) :
            movie_name = movie_list[i]
            stmt = select(main_table).where(main_table.movie_name == movie_name)
            data = session.scalars(stmt).first()
            if data == None :
                main_data = main_table(
                    movie_name = movie_name,
                    date = datetime(2025,9,1,0,0,0),
                    registed_date =datetime.now(),
                    person = "guest"
                )
                session.add(main_data)
        session.commit()
