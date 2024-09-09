from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class LeaveService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="leaves", id="id", jdbcDataSource=jdbcDataSource)


