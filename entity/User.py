from entity.Entity import Entity

class User(Entity):
    def __init__(self, user_id=None, emp_id=None, first_name=None, middle_name=None, last_name=None, email=None,
                 designation_id=None, designation_name=None, department_description=None, is_hr=None, is_supervisor=None):
        self.id: int = user_id
        self.emp_id: str = emp_id
        self.first_name: str = first_name
        self.middle_name: str = middle_name
        self.last_name: str = last_name
        self.email: str = email
        self.designation_id: int = designation_id
        self.designation_name: str = designation_name
        self.department_description: str = department_description
        self.is_hr: bool = is_hr
        self.is_supervisor: bool = is_supervisor
