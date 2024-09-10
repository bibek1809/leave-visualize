from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class StatusService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="Status", id="id", jdbcDataSource=jdbcDataSource)

    def update_previous_status(self,status_type,id_):
        return self.jdbcDataSource.cud_execute(f"""update Status set status = 4 where status_type = '{status_type}' and id < {id_} and status =1 """)
