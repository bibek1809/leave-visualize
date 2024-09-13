from entity.Entity import Entity

class Designation(Entity):
    def __init__(self, designation_id=None, designation_name=None):
        self.id: int = designation_id
        self.designation_name: str = designation_name
