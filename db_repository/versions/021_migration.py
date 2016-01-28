from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tea = Table('tea', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tea_category_id', Integer),
    Column('tea_name', String(length=20)),
    Column('tea_about', String(length=255)),
    Column('tea_price_400', Integer),
    Column('tea_price_800', Integer),
    Column('tea_price_1000', Integer),
)

tea_category = Table('tea_category', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tea_category_name', String(length=50)),
    Column('tea_img', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['tea'].create()
    post_meta.tables['tea_category'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['tea'].drop()
    post_meta.tables['tea_category'].drop()
