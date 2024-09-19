from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create tables
    op.create_table(
        'raw',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('emp_id', sa.String(255)),
        sa.Column('team_manager_id', sa.Integer),
        sa.Column('designation_id', sa.Integer),
        sa.Column('designation_name', sa.String(255)),
        sa.Column('first_name', sa.String(255)),
        sa.Column('middle_name', sa.String(255)),
        sa.Column('last_name', sa.String(255)),
        sa.Column('email', sa.String(255)),
        sa.Column('is_hr', sa.String(255)),
        sa.Column('is_supervisor', sa.String(255)),
        sa.Column('leave_issuer_id', sa.Integer),
        sa.Column('issuer_first_name', sa.String(255)),
        sa.Column('issuer_middle_name', sa.String(255)),
        sa.Column('issuer_last_name', sa.String(255)),
        sa.Column('current_leave_issuer_id', sa.Integer),
        sa.Column('current_leave_issuer_email', sa.String(255)),
        sa.Column('department_description', sa.String(255)),
        sa.Column('start_date', sa.Date),
        sa.Column('end_date', sa.Date),
        sa.Column('leave_days', sa.Integer),
        sa.Column('reason', sa.Text),
        sa.Column('leave_status', sa.String(255)),
        sa.Column('status', sa.String(255)),
        sa.Column('response_remarks', sa.Text),
        sa.Column('leave_type_id', sa.Integer),
        sa.Column('leave_type', sa.String(255)),
        sa.Column('default_days', sa.Integer),
        sa.Column('transferable_days', sa.Integer),
        sa.Column('is_consecutive', sa.String(255)),
        sa.Column('fiscal_id', sa.Integer),
        sa.Column('fiscal_start_date', sa.Date),
        sa.Column('fiscal_end_date', sa.Date),
        sa.Column('fiscal_is_current', sa.String(255)),
        sa.Column('created_at', sa.TIMESTAMP),
        sa.Column('updated_at', sa.TIMESTAMP),
        sa.Column('is_automated', sa.String(255)),
        sa.Column('is_converted', sa.String(255)),
        sa.Column('total_count', sa.Integer),
        sa.Column('inserted_at', sa.Date),
        sa.Column('allocations', sa.Text)
    )

    op.create_table(
        'employee',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('emp_id', sa.String(50)),
        sa.Column('first_name', sa.String(100)),
        sa.Column('middle_name', sa.String(100)),
        sa.Column('last_name', sa.String(100)),
        sa.Column('email', sa.String(100)),
        sa.Column('designation_id', sa.Integer),
        sa.Column('designation_name', sa.String(100)),
        sa.Column('department_description', sa.String(255)),
        sa.Column('is_hr', sa.Boolean),
        sa.Column('is_supervisor', sa.Boolean)
    )

    op.create_table(
        'leaves',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('leave_type', sa.String(100)),
        sa.Column('default_days', sa.Integer),
        sa.Column('transferable_days', sa.Integer),
        sa.Column('fiscal_id', sa.Integer),
        sa.Column('fiscal_start_date', sa.Date),
        sa.Column('fiscal_end_date', sa.Date),
        sa.Column('fiscal_is_current', sa.Boolean)
    )

    op.create_table(
        'leave_transactions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('leave_type_id', sa.Integer),
        sa.Column('start_date', sa.Date),
        sa.Column('end_date', sa.Date),
        sa.Column('leave_days', sa.Integer),
        sa.Column('reason', sa.String(255)),
        sa.Column('response_remarks', sa.String(255)),
        sa.Column('leave_status', sa.String(50)),
        sa.Column('is_converted', sa.Boolean),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
        sa.Column('current_leave_issuer_id', sa.Integer),
        sa.Column('issuer_first_name', sa.String(100)),
        sa.Column('issuer_middle_name', sa.String(100)),
        sa.Column('issuer_last_name', sa.String(100)),
        sa.Column('current_leave_issuer_email', sa.String(100)),
        sa.Column('is_consecutive', sa.Boolean),
        sa.Column('is_automated', sa.Boolean),
        sa.Column('department_description', sa.String(100)),
        sa.Column('designation_name', sa.String(100)),
        sa.Column('designation_id', sa.Integer),
        sa.Column('is_supervisor', sa.Boolean),
        sa.Column('is_hr', sa.Boolean)
    )

    op.create_table(
        'designation',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('designation_name', sa.String(255), nullable=False)
    )

    op.create_table(
        'status',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('status_type', sa.String(255), nullable=False),
        sa.Column('start_date', sa.Date),
        sa.Column('end_date', sa.Date),
        sa.Column('started_at', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('status', sa.Integer),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())
    )

def downgrade():
    # Drop tables if reverting the migration
    op.drop_table('status')
    op.drop_table('designation')
    op.drop_table('leave_transactions')
    op.drop_table('leaves')
    op.drop_table('employee')
    op.drop_table('raw')
