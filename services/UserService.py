from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class UserService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="users", id="id", jdbcDataSource=jdbcDataSource)


