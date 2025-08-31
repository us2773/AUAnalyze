from sqlalchemy import create_engine
from models import Base, main_table, au_table
import db_config

def register() :
    # Engine作成
    engine = create_engine(f"postgresql+psycopg2://{db_config.user_name}:{db_config.password}@{db_config.host_name}/facehealthdb",echo=True)
    # Table 作成
    Base.metadata.create_all(engine)
    for column in main_table.__table__.columns:
        print(column.name, column.type)
        
if __name__ == "__main__":
    register()