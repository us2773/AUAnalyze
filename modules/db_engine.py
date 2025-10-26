import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # modules の親を追加

from sqlalchemy import create_engine, select
from modules import db_config

engine = create_engine(f"postgresql+psycopg2://{db_config.user_name}:{db_config.password}@{db_config.host_name}/facehealthdb",echo=True)