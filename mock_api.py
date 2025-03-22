import uuid
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Mock Lead API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

leads_db = {}

class Lead(BaseModel):
    """This is the model for the lead. It is used to create a new lead."""
    name: str
    email: str
    phone: str
    leadSource: str
    notes: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Mock Lead API is running"}

@app.post("/api/admin/lead")
async def create_lead(lead: Dict[str, Any]):
    """Endpoint to create a new lead."""
    lead_id = str(uuid.uuid4())

    if not all(key in lead for key in ['name', 'email', 'phone', 'leadSource']):
        missing = [key for key in ['name', 'email', 'phone', 'leadSource'] if key not in lead]
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing)}")

    leads_db[lead_id] = lead

    print(f"Created lead: {lead_id}")
    print(f"Lead data: {lead}")

    return {"leadId": lead_id, "message": "Lead created successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
