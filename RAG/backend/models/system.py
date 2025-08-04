from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class SystemInfoResponse(BaseModel):
    vector_db: Dict[str, Any]
    ai_model: Dict[str, Any]
    system_status: str
    error_message: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0" 