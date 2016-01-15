from sqlalchemy import *
from migrate.versioning import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
category = Table('category', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('category_name', String(length=50)),
    Column('alias', String(length=50)),
    Column('sous', Boolean, default=ColumnDefault(False)),
    Column('cafe', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['category'].columns['sous'].create()
    post_meta.tables['category'].columns['cafe'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['category'].columns['sous'].drop()
    post_meta.tables['category'].columns['cafe'].drop()
