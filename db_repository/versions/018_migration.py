from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
items = Table('items', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item_name', String(length=50)),
    Column('item_component', String(length=50)),
    Column('category_id', Integer),
    Column('weight', String(length=50)),
    Column('price', String(length=50), default=ColumnDefault(0)),
    Column('img', String(length=50)),
    Column('thumbnail', String(length=255)),
    Column('cafe_only', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['items'].columns['cafe_only'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['items'].columns['cafe_only'].drop()
