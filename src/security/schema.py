from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Credentials:
    user_id: uuid.UUID
    issued_at: datetime | None = None
    expires_at: datetime | None = None
