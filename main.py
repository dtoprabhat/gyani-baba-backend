from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from pypdf import PdfReader

app = FastAPI(title="Gyani Baba Knowledge Backend with PDF Upload")

# Enable CORS taaki Google Sites se ye API connect ho sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gyani Baba Memory Database (Initial Memory)
GYANI_MEMORY = [
    {
        "topic": "leave rules", 
        "content": "As per Circular No. 102/2025, casual leave can be availed up to 15 days per year with prior approval."
    },
    {
        "topic": "transfer policy", 
        "content": "Office Memorandum 2026 states that routine transfers will take place strictly in the month of May."
    }
]

class QueryRequest(BaseModel):
    prompt: str

# 1. PDF Upload karke Memory Update karne ka endpoint
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Kripya sirf PDF file upload karein.")
    
    try:
        # PDF ko read karna
        reader = PdfReader(file.file)
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        
        # Memory mein naye document ko jorna
        topic_name = file.filename.replace(".pdf", "").replace("_", " ").lower()
        GYANI_MEMORY.append({
            "topic": topic_name,
            "content": extracted_text[:1500] # Pehle 1500 characters store honge
        })
        
        return {"status": "success", "message": f"'{file.filename}' safaltapurvak Gyani Baba ki memory mein jodh diya gaya hai!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File read karne mein samasya aayi: {str(e)}")

# 2. Chat Query Endpoint
@app.post("/chat")
def chat_with_gyani(request: QueryRequest):
    user_query = request.prompt.lower().strip()
    
    # Greetings check
    greetings = ["hi", "hello", "hey", "namaste", "pranam", "good morning", "good evening", "kaise ho"]
    if any(greet in user_query for greet in greetings):
        return {
            "answer": "Kalyan ho! Main Gyani Baba hoon. Aap mujhse kisi bhi sarkari circular, notification, act ya rule ke baare mein pooch sakte hain. Batayein, aaj kis vishay par charcha karni hai?"
        }

    # Search in Memory
    matched_info = None
    for item in GYANI_MEMORY:
        if any(keyword in user_query for keyword in item["topic"].split()):
            matched_info = item["content"]
            break
            
    if matched_info:
        answer = f"Gyani Baba ke abhilekh ke anusar: {matched_info}"
    else:
        answer = "Ye suchna mere paas abhi uplabdh nahi hai, main isse seekh raha hoon."
        
    return {"answer": answer}
