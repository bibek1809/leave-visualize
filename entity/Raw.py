from entity.Entity import Entity

class Raw(Entity):
    def __init__(self, id=None, user_id=None, emp_id=None, start_date=None, end_date=None, leave_days=None, reason=None,
                 response_remarks=None, leave_type_id=None, default_days=None, transferable_days=None, fiscal_year_id=None,
                 fiscal_year_start_date=None, fiscal_year_end_date=None, fiscal_is_current=None, is_converted=None, created_at=None,
                 updated_at=None, leave_status=None, leave_type=None, first_name=None, middle_name=None, last_name=None,
                 email=None, current_leave_issuer_email=None, designation_id=None, designation_name=None, 
                 department_description=None, is_hr=None, is_supervisor=None, is_consecutive=None, current_leave_issuer_id=None, 
                 issuer_first_name=None, issuer_middle_name=None, issuer_last_name=None, applied_before=None, is_automated=None):
        
        self.id: int = id
        self.user_id: int = user_id
        self.emp_id: str = emp_id
        self.start_date = start_date
        self.end_date = end_date
        self.leave_days: int = leave_days
        self.reason: str = reason
        self.response_remarks: str = response_remarks
        self.leave_type_id: int = leave_type_id
        self.default_days: int = default_days
        self.transferable_days: int = transferable_days
        self.fiscal_year_id: int = fiscal_year_id
        self.fiscal_year_start_date = fiscal_year_start_date
        self.fiscal_year_end_date = fiscal_year_end_date
        self.fiscal_is_current: bool = fiscal_is_current
        self.is_converted: bool = is_converted
        self.created_at = created_at
        self.updated_at = updated_at
        self.leave_status: str = leave_status
        self.leave_type: str = leave_type
        self.first_name: str = first_name
        self.middle_name: str = middle_name
        self.last_name: str = last_name
        self.email: str = email
        self.current_leave_issuer_email: str = current_leave_issuer_email
        self.designation_id: int = designation_id
        self.designation_name: str = designation_name
        self.department_description: str = department_description
        self.is_hr: bool = is_hr
        self.is_supervisor: bool = is_supervisor
        self.is_consecutive: bool = is_consecutive
        self.current_leave_issuer_id: int = current_leave_issuer_id
        self.issuer_first_name: str = issuer_first_name
        self.issuer_middle_name: str = issuer_middle_name
        self.issuer_last_name: str = issuer_last_name
        self.applied_before: bool = applied_before
        self.is_automated: bool = is_automated
