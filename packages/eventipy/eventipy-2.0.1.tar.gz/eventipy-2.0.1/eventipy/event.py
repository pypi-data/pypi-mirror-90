from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Event:
    topic: str
    id: UUID = field(default_factory=uuid4, init=False)
    created_at: datetime = field(default_factory=datetime.now, init=False)
