from database.JdbcDataSource import JdbcDataSource
from services.JDBCRepository import JDBCRepository


class RawService(JDBCRepository):

    def __init__(self, jdbcDataSource: JdbcDataSource) -> None:
        super().__init__(entity_name="raw", id="id", jdbcDataSource=jdbcDataSource)

    def get_data_count(self,date,type=None):
        if type == 'user':
            return self.jdbcDataSource.execute(f"""select count(*) as total_count from (SELECT
                    distinct
                    user_id,
                    emp_id,
                    first_name,
                    middle_name,
                    last_name,
                    email,
                    designation_id,
                    designation_name,
                    department_description,
                    CASE WHEN is_hr = 'True' THEN 1 ELSE 0 END AS is_hr,
                    CASE WHEN is_supervisor = 'True' THEN 1 ELSE 0 END AS is_supervisor
                FROM raw
                WHERE inserted_at = '{date}') as tt""")
        elif type == 'leave':
            return self.jdbcDataSource.execute(f"""select count(*) as total_count from (SELECT
                                        distinct
                    leave_type_id,
                    leave_type,
                    default_days,
                    transferable_days,
                    fiscal_id,
                    fiscal_start_date,
                    fiscal_end_date,
                    CASE WHEN fiscal_is_current = 'True' THEN 1 ELSE 0 END AS fiscal_is_current
                FROM raw
                WHERE inserted_at = '{date}') as tt""")
        elif type == 'designation':
            return self.jdbcDataSource.execute(f"""select count(*) as total_count from (SELECT
                distinct designation_name,designation_id
                FROM raw
                WHERE inserted_at = '{date}') as tt""")

        return self.jdbcDataSource.execute(f"""select count(1) as total_count from raw where inserted_at = '{date}' """)

    def get_user_data(self, date,position):
        return self.jdbcDataSource.execute(f"""SELECT
                    distinct
                    user_id,
                    emp_id,
                    first_name,
                    middle_name,
                    last_name,
                    email,
                    designation_id,
                    designation_name,
                    department_description,
                    CASE WHEN is_hr = 'True' THEN 1 ELSE 0 END AS is_hr,
                    CASE WHEN is_supervisor = 'True' THEN 1 ELSE 0 END AS is_supervisor
                FROM raw
                WHERE inserted_at = '{date}'
                limit {position},10000
                    """)

    def get_leave_data(self, date, position):
        return self.jdbcDataSource.execute(f"""SELECT
                                           distinct
                    leave_type_id,
                    leave_type,
                    default_days,
                    transferable_days,
                    fiscal_id,
                    fiscal_start_date,
                    fiscal_end_date,
                    CASE WHEN fiscal_is_current = 'True' THEN 1 ELSE 0 END AS fiscal_is_current
                FROM raw
                WHERE inserted_at = '{date}'
                LIMIT {position}, 10000
                    """)

    def get_transaction_data(self, date, position):
        return self.jdbcDataSource.execute(f"""SELECT
                    id,
                    user_id,
                    leave_type_id,
                    start_date,
                    end_date,
                    leave_days,
                    left(reason,200) as reason,
                    response_remarks,
                    leave_status,
                    CASE WHEN is_converted = 'True' THEN 1 ELSE 0 END AS is_converted,
                    created_at,
                    updated_at,
                    current_leave_issuer_id,
                    issuer_first_name,
                    issuer_middle_name,
                    issuer_last_name,
                    current_leave_issuer_email,
                    CASE WHEN is_consecutive = 'True' THEN 1 ELSE 0 END AS is_consecutive,
                    CASE WHEN is_automated = 'True' THEN 1 ELSE 0 END AS is_automated,
                    department_description,designation_name,designation_id,
                        CASE WHEN team_manager_id is NUll  THEN 1 ELSE 0 END AS is_supervisor,
                    CASE WHEN is_hr = 'True' THEN 1 ELSE 0 END AS is_hr
                FROM raw
                WHERE inserted_at = '{date}'
                group by id
                LIMIT {position}, 10000
                    """)

    def get_designation_data(self, date, position):
        return self.jdbcDataSource.execute(f"""SELECT
                distinct designation_id,designation_name
                FROM raw
                WHERE inserted_at = '{date}'
                LIMIT {position}, 10000
                    """)