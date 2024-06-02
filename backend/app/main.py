from fastapi import FastAPI, File, UploadFile, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import fitz  # PyMuPDF
import shutil
from datetime import datetime, timezone
from app.nlp import initialize_query_engine  
from app.database import SessionLocal, engine
from app import crud, models

# Initialize the NLP model query engine
query_engine = initialize_query_engine()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:3000',
    'https://frontendpdf-retb61ah1-maanit-aroras-projects.vercel.app/'
]

# Enabling CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

def extract_text_and_metadata(file_path: str):
    try:
        document = fitz.open(file_path)
        pdf_metadata = document.metadata
        num_pages = document.page_count
        text = ""
        
        for page_num in range(num_pages):
            page = document.load_page(page_num)
            text += page.get_text()

        return {
            "metadata": pdf_metadata,
            "num_pages": num_pages,
            "text": text
        }
    except Exception as e:
        print(f"Error extracting text and metadata from PDF: {e}")
        return None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs("uploaded_files", exist_ok=True)
    
    # Validate file type
    if file.content_type != 'application/pdf':
        return JSONResponse({"error": "Unsupported file type. Please upload a PDF file."}, status_code=400)
    
    # Deleting any existing files in the directory
    folder = 'uploaded_files'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    try:
        file_path = os.path.join(folder, file.filename)
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
        
        extraction_result = extract_text_and_metadata(file_path)
        if extraction_result is None:
            return JSONResponse({"error": "Error extracting text and metadata from PDF."}, status_code=500)
        
        pdf_info = crud.create_pdf_info(
            db=db,
            filename=file.filename,
            pdf_metadata=str(extraction_result["metadata"]),
            num_pages=extraction_result["num_pages"]
        )
        
        # Reinitializing the NLP model with the new document
        global query_engine
        query_engine = initialize_query_engine()

        return JSONResponse({
            "message": f"File uploaded successfully: {file.filename}",
            "filename": f"{file.filename}"
        })
    except Exception as e:
        print(f"Error uploading file: {e}")
        return JSONResponse({"error": "Error uploading file."}, status_code=500)

@app.post("/api/query")
async def ask(request: QueryRequest):
    print("Received query request")
    folder = 'uploaded_files'
    
    # Checking if the uploaded_files directory is empty
    if not os.listdir(folder):
        print("No files found in the uploaded_files directory")
        return JSONResponse({"error": "No files found in the uploaded_files directory."}, status_code=400)

    # Checking if the NLP model (query_engine) is initialized
    if query_engine is None:
        print("NLP model has not been initialized")
        return JSONResponse({"error": "The NLP model has not been initialized."}, status_code=500)

    try:
        # Processing the user's query using your NLP model
        print(f"Processing query: {request.question}")
        llama_type_answer = query_engine.query(request.question)
        answer = str(llama_type_answer)
        if answer == "Empty Response":
            print("Empty response from NLP model")
            return JSONResponse({"answer": "I am sorry I couldn't comprehend:( Could you please ask the whole question again?"})

        print(f"Query processed successfully: {answer}")
        return JSONResponse({"answer": answer})
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
