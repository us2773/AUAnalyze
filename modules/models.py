from sqlalchemy.orm import DeclarativeBase, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Text, Uuid, DateTime, Integer, Float, ForeignKey

class Base(DeclarativeBase):
    pass

class main_table(Base) :
    __tablename__ = "main_table"
    id = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    movie_name = mapped_column(Text, unique=True)
    date = mapped_column(DateTime(timezone=True))
    # fatigue_level = mapped_column(ARRAY(Float))
    registed_date = mapped_column(DateTime)
    person = mapped_column(Text)
    
class au_table(Base) :
    __tablename__ = "AU_table"
    indiv_id = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    data_id = mapped_column(ForeignKey("main_table.id"), unique=True,nullable=False)
    trend_mean = mapped_column(ARRAY(Float))
    trend_var = mapped_column(ARRAY(Float))
    noise_mean = mapped_column(ARRAY(Float))
    noise_var = mapped_column(ARRAY(Float))
    num_of_peak = mapped_column(ARRAY(Integer))
    peak_freq = mapped_column(ARRAY(Float))
    