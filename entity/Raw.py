from datetime import datetime
from entity.Entity import Entity
import json

class Raw(Entity):
    def __init__(self, id=None, user_id=None, emp_id=None, team_manager_id=None, designation_id=None, designation_name=None, 
                 first_name=None, middle_name=None, last_name=None, email=None, is_hr=None, is_supervisor=None, 
                 leave_issuer_id=None, issuer_first_name=None, issuer_middle_name=None, issuer_last_name=None, 
                 current_leave_issuer_id=None, current_leave_issuer_email=None, department_description=None, 
                 start_date=None, end_date=None, leave_days=None, reason=None, leave_status=None, status=None, 
                 response_remarks=None, leave_type_id=None, leave_type=None, default_days=None, transferable_days=None, 
                 is_consecutive=None, fiscal_id=None, fiscal_start_date=None, fiscal_end_date=None, fiscal_is_current=None, 
                 created_at=None, updated_at=None, is_automated=None, is_converted=None, total_count=None, allocations=None,inserted_at=None):
        
        # Integer Fields
        self.id: int = self.to_int(id)
        self.user_id: int = self.to_int(user_id)
        
        # Convert all other integer fields to strings
        self.emp_id: str = str(emp_id) if emp_id is not None else None
        self.team_manager_id: str = str(team_manager_id) if team_manager_id is not None else None
        self.designation_id: str = str(designation_id) if designation_id is not None else None
        self.leave_days: str = str(leave_days) if leave_days is not None else None
        self.leave_type_id: str = str(leave_type_id) if leave_type_id is not None else None
        self.total_count: str = str(total_count) if total_count is not None else None
        self.is_consecutive: str = str(is_consecutive) if is_consecutive is not None else None
        self.fiscal_id: str = str(fiscal_id) if fiscal_id is not None else None
        self.is_automated: str = str(is_automated) if is_automated is not None else None
        self.is_converted: str = str(is_converted) if is_converted is not None else None

        # String Fields
        self.designation_name: str = str(designation_name) if designation_name is not None else None
        self.first_name: str = str(first_name) if first_name is not None else None
        self.middle_name: str = str(middle_name) if middle_name is not None else None
        self.last_name: str = str(last_name) if last_name is not None else None
        self.email: str = str(email) if email is not None else None
        self.is_hr: str = str(is_hr) if is_hr is not None else None
        self.is_supervisor: str = str(is_supervisor) if is_supervisor is not None else None
        self.leave_issuer_id: str = str(leave_issuer_id) if leave_issuer_id is not None else None
        self.issuer_first_name: str = str(issuer_first_name) if issuer_first_name is not None else None
        self.issuer_middle_name: str = str(issuer_middle_name) if issuer_middle_name is not None else None
        self.issuer_last_name: str = str(issuer_last_name) if issuer_last_name is not None else None
        self.current_leave_issuer_id: str = str(current_leave_issuer_id) if current_leave_issuer_id is not None else None
        self.current_leave_issuer_email: str = str(current_leave_issuer_email) if current_leave_issuer_email is not None else None
        self.department_description: str = str(department_description) if department_description is not None else None
        self.reason: str = str(reason) if reason is not None else None
        self.leave_status: str = str(leave_status) if leave_status is not None else None
        self.status: str = str(status) if status is not None else None
        self.response_remarks: str = str(response_remarks) if response_remarks is not None else None
        self.leave_type: str = str(leave_type) if leave_type is not None else None
        self.default_days: str = str(default_days) if default_days is not None else None
        self.transferable_days: str = str(transferable_days) if transferable_days is not None else None
        self.fiscal_is_current: str = str(fiscal_is_current) if fiscal_is_current is not None else None
        
        # Date Fields
        self.start_date: datetime = self.parse_iso_format(start_date)
        self.end_date: datetime = self.parse_iso_format(end_date)
        self.fiscal_start_date: datetime = self.parse_iso_format(fiscal_start_date)
        self.fiscal_end_date: datetime = self.parse_iso_format(fiscal_end_date)
        self.created_at: datetime = self.parse_iso_format(created_at)
        self.updated_at: datetime = self.parse_iso_format(updated_at)
        self.inserted_at:datetime = datetime.now().date()
        # JSON Allocation
        self.allocations: list = self.parse_allocations(allocations)

    @staticmethod
    def parse_iso_format(date_str):
        """Parses a date string, supporting both '%Y-%m-%d' and '%Y-%m-%dT%H:%M:%S.%fZ' formats."""
        if not date_str:
            return None
        
        formats = ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S']
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Date format of '{date_str}' is not recognized.")
    
    @staticmethod
    def to_int(value):
        """Converts a value to an integer, if possible."""
        try:
            return int(value) if value is not None else None
        except (ValueError, TypeError):
            raise ValueError(f"Value '{value}' cannot be converted to int.")

    @staticmethod
    def parse_allocations(allocations):
        if allocations is None:
            return {}
        """Converts allocations to JSON if it's a valid list or dictionary."""
        if isinstance(allocations, str):
            try:
                return json.loads(allocations)
            except json.JSONDecodeError:
                raise ValueError(f"Allocations string '{allocations}' cannot be parsed as JSON.")
        elif isinstance(allocations, list) or isinstance(allocations, dict):
            return allocations
        else:
            raise ValueError(f"Allocations value '{allocations}' is not a valid JSON string, list, or dictionary.")
