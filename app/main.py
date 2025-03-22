import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Lead Extraction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Lead Extraction API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=os.getenv("API_HOST", "0.0.0.0"), 
        port=int(os.getenv("API_PORT", "8000")),
        reload=True
    ) 