from sqlalchemy.orm import Session
from .models import PDFInfo
from datetime import datetime, timezone

def create_pdf_info(db: Session, filename: str, pdf_metadata: str, num_pages: int):
    db_pdf_info = PDFInfo(
        filename=filename,
        pdf_metadata=pdf_metadata,
        num_pages=num_pages,
        upload_timestamp=datetime.now(timezone.utc)
    )
    db.add(db_pdf_info)
    db.commit()
    db.refresh(db_pdf_info)
    return db_pdf_info
