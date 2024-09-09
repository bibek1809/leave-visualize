from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class LeaveTxnService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="leave_transactions", id="id", jdbcDataSource=jdbcDataSource)


