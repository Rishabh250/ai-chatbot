from fastapi import APIRouter, Request, HTTPException, Depends
from langchain.chains.llm import LLMChain
from app.services.langchain_agent import llm, lead_prompt, lead_parser, ai_response_on_missing_info
from app.services.chat_memory import session_manager
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

@router.post("/")
async def chat(request: Request):
    try:
        body = await request.json()
        message = body.get("message")

        # Get or generate user_id
        user_id = body.get("user_id")
        if not user_id:
            user_id = str(uuid.uuid4())

        if not message:
            return {"response": "Please provide a message", "user_id": user_id}

        memory = session_manager.get_memory(user_id)
        collector = session_manager.get_lead_collector(user_id)

        memory.chat_memory.add_user_message(message)

        chain = LLMChain(
            llm=llm,
            prompt=lead_prompt,
            output_parser=lead_parser
        )

        try:
            parsed_data = chain.run(message=message)

            if hasattr(parsed_data, 'dict'):
                parsed_data = parsed_data.dict()

            collector.update_data(parsed_data)

        except Exception as e:
            error_message = f"Sorry, I didn't get that. Can you rephrase? Error: {str(e)}"
            memory.chat_memory.add_ai_message(error_message)
            return {"response": error_message, "user_id": user_id}

        if collector.is_ready():
            lead_id = collector.submit()
            success_message = "✅ Lead created successfully!"
            memory.chat_memory.add_ai_message(success_message)
            return {"response": success_message, "leadId": lead_id, "user_id": user_id}

        missing = collector.get_missing_fields()
        missing_pretty = ", ".join(missing)

        response_chain = LLMChain(
            llm=llm,
            prompt=ai_response_on_missing_info
        )

        response_text = response_chain.run(message=message, missing_fields=missing_pretty)

        if hasattr(response_text, 'content'):
            response_text = response_text.content
        
        memory.chat_memory.add_ai_message(response_text)

        return {"response": response_text, "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions")
async def list_sessions():
    """
    List all active user sessions
    """
    active_sessions = session_manager.list_active_sessions()
    return {"active_sessions": active_sessions, "count": len(active_sessions)}

@router.delete("/session/{user_id}")
async def clear_session(user_id: str):
    """
    Clear a specific user's session
    """
    session_manager.clear_session(user_id)
    return {"message": f"Session for user {user_id} cleared successfully"}

@router.get("/history/{user_id}")
async def get_history(user_id: str):
    """
    Get conversation history for a specific user
    """
    try:
        memory = session_manager.get_memory(user_id)
        return {"history": memory.chat_memory.messages, "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User session not found: {str(e)}")