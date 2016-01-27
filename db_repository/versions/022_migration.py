from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
adress = Table('adress', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('address', TEXT),
)

adress = Table('adress', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('select_region', String(length=50)),
    Column('street', String(length=50)),
    Column('home', String(length=50)),
    Column('home_corp', String(length=50)),
    Column('porch', String(length=50)),
    Column('domofon', String(length=50)),
    Column('floor', String(length=50)),
    Column('kvartira', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['adress'].columns['address'].drop()
    post_meta.tables['adress'].columns['domofon'].create()
    post_meta.tables['adress'].columns['floor'].create()
    post_meta.tables['adress'].columns['home'].create()
    post_meta.tables['adress'].columns['home_corp'].create()
    post_meta.tables['adress'].columns['kvartira'].create()
    post_meta.tables['adress'].columns['porch'].create()
    post_meta.tables['adress'].columns['select_region'].create()
    post_meta.tables['adress'].columns['street'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['adress'].columns['address'].create()
    post_meta.tables['adress'].columns['domofon'].drop()
    post_meta.tables['adress'].columns['floor'].drop()
    post_meta.tables['adress'].columns['home'].drop()
    post_meta.tables['adress'].columns['home_corp'].drop()
    post_meta.tables['adress'].columns['kvartira'].drop()
    post_meta.tables['adress'].columns['porch'].drop()
    post_meta.tables['adress'].columns['select_region'].drop()
    post_meta.tables['adress'].columns['street'].drop()
