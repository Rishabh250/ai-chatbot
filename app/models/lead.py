from pydantic import BaseModel, Field
from typing import Optional

class LeadForm(BaseModel):
    """
    Model for lead information collected from users.
    """
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None 
    phone: Optional[str] = None
    leadSource: Optional[str] = None
    
    def dict(self, **kwargs):
        # Filter out None values before returning dict
        result = super().dict(**kwargs)
        return {k: v for k, v in result.items() if v is not None} 