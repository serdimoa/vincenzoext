from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
saleo_on_time = Table('saleo_on_time', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('sale_name', String(length=255)),
    Column('down_sale', String(length=20)),
    Column('date_sale_on', String(length=255)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['saleo_on_time'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['saleo_on_time'].drop()
