from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
adress = Table('adress', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('adress', VARCHAR(length=50)),
)

adress = Table('adress', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('address', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['adress'].columns['adress'].drop()
    post_meta.tables['adress'].columns['address'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['adress'].columns['adress'].create()
    post_meta.tables['adress'].columns['address'].drop()
