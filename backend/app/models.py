from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class PDFInfo(Base):
    __tablename__ = "pdf_info"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    pdf_metadata = Column(Text)
    num_pages = Column(Integer)
    upload_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
