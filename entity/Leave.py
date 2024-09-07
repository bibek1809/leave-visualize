from entity.Entity import Entity

class Leave(Entity):
    def __init__(self, leave_type_id=None, leave_type=None, default_days=None, transferable_days=None,
                 fiscal_year_id=None, fiscal_year_start_date=None, fiscal_year_end_date=None, fiscal_is_current=None):
        self.leave_type_id: int = leave_type_id
        self.leave_type: str = leave_type
        self.default_days: int = default_days
        self.transferable_days: int = transferable_days
        self.fiscal_year_id: int = fiscal_year_id
        self.fiscal_year_start_date = fiscal_year_start_date
        self.fiscal_year_end_date = fiscal_year_end_date
        self.fiscal_is_current: bool = fiscal_is_current
