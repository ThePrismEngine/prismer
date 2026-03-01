from sqlalchemy import Column, Integer, Text, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Version(Base):
    __tablename__ = "version"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    published_at = Column(Date, nullable=False)
    path = Column(Text, nullable=False)
    install_at = Column(Date, nullable=False)

    def __str__(self):
        return f"{self.tag}({self.name})"