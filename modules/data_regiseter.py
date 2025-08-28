from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, main_table
import db_config

def main() :
    # Engine作成
    engine = create_engine(f"postgresql+psycopg2://{db_config.user_name}:{db_config.password}@{db_config.host_name}/facehealthdb",echo=True)
    Base.metadata.create_all(engine)
    for column in main_table.__table__.columns:
        print(column.name, column.type)
        
if __name__ == "__main__":
    main()