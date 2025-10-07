import sqlalchemy as sa
from clickhouse_sqlalchemy import engines

_metadata = sa.MetaData()

users = sa.Table(
    "user_account",
    _metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(30), nullable=False),
    sa.Column("fullname", sa.String(30)),
    engines.MergeTree(order_by="id"),
)

addresses = sa.Table(
    "address",
    _metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email_address", sa.String(30), nullable=False),
    sa.Column("user_id", sa.ForeignKey("user_account.id"), nullable=False),
    engines.MergeTree(order_by="id"),
)
