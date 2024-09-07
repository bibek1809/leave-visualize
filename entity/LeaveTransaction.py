from entity.Entity import Entity

class LeaveTransaction(Entity):
    def __init__(self, id=None, user_id=None, leave_type_id=None, start_date=None, end_date=None, leave_days=None,
                 reason=None, response_remarks=None, leave_status=None, is_converted=None, created_at=None, updated_at=None,
                 current_leave_issuer_id=None, issuer_first_name=None, issuer_middle_name=None, issuer_last_name=None,
                 current_leave_issuer_email=None, is_consecutive=None, applied_before=None, is_automated=None):
        self.id: int = id
        self.user_id: int = user_id
        self.leave_type_id: int = leave_type_id
        self.start_date = start_date
        self.end_date = end_date
        self.leave_days: int = leave_days
        self.reason: str = reason
        self.response_remarks: str = response_remarks
        self.leave_status: str = leave_status
        self.is_converted: bool = is_converted
        self.created_at = created_at
        self.updated_at = updated_at
        self.current_leave_issuer_id: int = current_leave_issuer_id
        self.issuer_first_name: str = issuer_first_name
        self.issuer_middle_name: str = issuer_middle_name
        self.issuer_last_name: str = issuer_last_name
        self.current_leave_issuer_email: str = current_leave_issuer_email
        self.is_consecutive: bool = is_consecutive
        self.applied_before: bool = applied_before
        self.is_automated: bool = is_automated
