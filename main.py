from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Gyani Baba Knowledge Backend")

# Enable CORS taaki Google Sites se ye API connect ho sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# GYANI BABA MEMORY (Yahan aap apne naye rules/circulars add kar sakte hain)
# ==========================================
GYANI_MEMORY = [
    {
        "topic": "leave rules", 
        "content": "As per Circular No. 102/2025, casual leave can be availed up to 15 days per year with prior approval."
    },
    {
        "topic": "transfer policy", 
        "content": "Office Memorandum 2026 states that routine transfers will take place strictly in the month of May."
    },
    # Aap yahan apna naya circular ya rule is tarah aage jodh sakte hain:
    # {
    #     "topic": "apne topic ka naam ya keyword likhein", 
    #     "content": "Yahan us circular ya rule ki poori jankari likhein."
    # }
]

class QueryRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat_with_gyani(request: QueryRequest):
    user_query = request.prompt.lower().strip()
    
    # 1. Basic Greetings Check (Hi, Hello, Namaste, Pranam, etc.)
    greetings = ["hi", "hello", "hey", "namaste", "pranam", "good morning", "good evening", "kaise ho", "kya हाल hai"]
    if any(greet in user_query for greet in greetings):
        return {
            "answer": "Kalyan ho! Main Gyani Baba hoon. Aap mujhse kisi bhi sarkari circular, notification, act ya rule ke baare mein pooch sakte hain. Batayein, aaj kis vishay par charcha karni hai?"
        }

    # 2. Search in Gyani Baba Memory
    matched_info = None
    for item in GYANI_MEMORY:
        if any(keyword in user_query for keyword in item["topic"].split()):
            matched_info = item["content"]
            break
            
    if matched_info:
        answer = f"Gyani Baba ke abhilekh ke anusar: {matched_info}"
    else:
        # Strict Guardrail jab memory mein data na ho
        answer = "Ye suchna mere paas abhi uplabdh nahi hai, main isse seekh raha hoon."
        
    return {"answer": answer}
