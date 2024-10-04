from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class UserService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="employee", id="id", jdbcDataSource=jdbcDataSource)

    def find_user_data(self,user_name = None):
        # If there are additional filter parameters, process them
        if user_name is not None:
            filters = f"""where tt.full_name like '%{user_name}%' """
        else:
            filters = ''
        sql_query = f"""select * from 
        (SELECT  emp_id, CONCAT(first_name, 
       CASE 
           WHEN middle_name IS NOT NULL AND middle_name <> '' THEN CONCAT(' ', middle_name) 
           ELSE '' 
       END, 
       ' ', 
       last_name)
         as full_name, email, designation_name, department_description, is_hr, is_supervisor
        FROM Attendence_System.employee ) as tt
        {filters} 
        """

        return self.jdbcDataSource.execute(sql_query)


