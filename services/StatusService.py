from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class StatusService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="Status", id="id", jdbcDataSource=jdbcDataSource)


