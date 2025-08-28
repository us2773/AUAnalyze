from sqlalchemy.orm import DeclarativeBase, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import ForeignKey, Text, Uuid, DateTime, Date, Float

class Base(DeclarativeBase):
    pass

class main_table(Base) :
    __tablename__ = "main_table"
    id = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    movie_name = mapped_column(Text, unique=True)
    date = mapped_column(DateTime)
    fatigue_level = mapped_column(ARRAY(Float))
    person = mapped_column(Text)