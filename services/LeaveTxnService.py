from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class LeaveTxnService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="leave_transactions", id="id", jdbcDataSource=jdbcDataSource)


    def find_leave_balance(self,emp_id=None):
        if not emp_id:
            sql_query = ''
        else:
            sql_query = f'''and  emp_id in ({emp_id}) '''
        return self.jdbcDataSource.execute(f"""select 
            e.emp_id ,
            e.leave_type,
            COALESCE (case when (e.default_days+ e.transferable_days) < TT.leave_taken
            then e.default_days+ e.transferable_days
            else TT.leave_taken end
            ,0) as leave_taken,
            e.default_days+ e.transferable_days  as total_leave,
            COALESCE (case when (e.default_days+ e.transferable_days) > TT.leave_taken
            then e.default_days+ e.transferable_days - TT.leave_taken
            when isnull(TT.leave_taken) then e.default_days+ e.transferable_days 
            else 0 end
            ,0) as available_leave
            from (select e.emp_id ,m.leave_type,m.default_days,m.transferable_days from  
            Attendence_System.employee e 
            join Attendence_System.leaves m) as e
            left join 
            (SELECT user_id,leave_type_id,sum(leave_days) as leave_taken FROM Attendence_System.leave_transactions
            where leave_status  = 'APPROVED'
            GROUP BY 1,2 ) AS TT
            on TT.user_id = e.emp_id 
            where e.leave_type != 'Leave Without Pay'
            {sql_query} """)

    def find_data(self, start,end,filter_params=None):
        if start is None:
            start = '2024-01-01'
        if end is None:
            end = '2024-09-10'
        # Build the base query
        sql_query = f"SELECT * FROM leave_transactions WHERE start_date BETWEEN '{start}' AND '{end}'"

        # If there are additional filter parameters, process them
        if filter_params:
            where_clauses = []
            for key, value in filter_params.items():
                if key not in ['start_date', 'end_date'] and value is not None:
                    where_clauses.append(f"{key}={self.convert(value)}")
            
            if where_clauses:
                # Join additional conditions with AND
                sql_query += " AND " + " AND ".join(where_clauses)

        # Append ORDER BY and LIMIT clauses
        sql_query += " ORDER BY 1 DESC LIMIT 30000"
        
        return self.jdbcDataSource.execute(sql_query)

