from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class LeaveTxnService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="leave_transactions", id="id", jdbcDataSource=jdbcDataSource)


    def find_data(self,start,end,para):
        if start is None:
            start = '2024-01-01'
        if end is None:
            end = '2024-09-10'
        return self.jdbcDataSource.execute(f"""select * from  leave_transactions where start_date between '{start}' and '{end}' 
         order by 1 desc limit 30000 """)

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

