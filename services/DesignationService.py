from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class DesignationService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="designation", id="id", jdbcDataSource=jdbcDataSource)
