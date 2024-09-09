from entity.Entity import Entity

class Status(Entity):
    def __init__(self, id=None, status_type=None, start_date=None, end_date=None, started_at=None, status=None):
        self.id: int = id
        self.status_type: str = status_type
        self.start_date: str = start_date  # Nullable
        self.end_date: str = end_date      # Nullable
        self.status: int = status          # Assuming this is an integer representing some status code
