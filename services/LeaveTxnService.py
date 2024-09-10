from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class LeaveTxnService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="leave_transactions", id="id", jdbcDataSource=jdbcDataSource)


    def find_data(self,start,end):
        if start is None:
            start = '2021-01-10'
        if end is None:
            end = '2024-01-10'
        return self.jdbcDataSource.execute(f"""select * from  leave_transactions where start_date between '{start}' and '{end}' 
         order by 1 desc limit 30000 """)

