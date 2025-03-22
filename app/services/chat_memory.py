from typing import Dict, List, Optional, Tuple
from langchain.memory import ConversationBufferMemory
from app.services.lead_client import LeadDataCollector

class ChatSessionManager:
    """
    Manages multiple chat sessions with memory for different users.
    Each user has their own conversation history and lead data collector.
    """
    def __init__(self):
        self.sessions: Dict[str, Tuple[ConversationBufferMemory, LeadDataCollector]] = {}

    def get_or_create_session(self, user_id: str) -> Tuple[ConversationBufferMemory, LeadDataCollector]:
        """
        Get an existing session for a user or create a new one if it doesn't exist.
        """
        if user_id not in self.sessions:
            # Create a new memory and lead collector for this user
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            lead_collector = LeadDataCollector()
            self.sessions[user_id] = (memory, lead_collector)

        return self.sessions[user_id]

    def get_memory(self, user_id: str) -> ConversationBufferMemory:
        """
        Get the conversation memory for a specific user.
        """
        return self.get_or_create_session(user_id)[0]

    def get_lead_collector(self, user_id: str) -> LeadDataCollector:
        """
        Get the lead data collector for a specific user.
        """
        return self.get_or_create_session(user_id)[1]

    def clear_session(self, user_id: str) -> None:
        """
        Clear a user's session (both memory and lead data).
        """
        if user_id in self.sessions:
            del self.sessions[user_id]

    def list_active_sessions(self) -> List[str]:
        """
        List all active user sessions.
        """
        return list(self.sessions.keys())

session_manager = ChatSessionManager() 
