from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('password', String(length=120)),
    Column('gender', String),
    Column('data', String),
    Column('height', String),
    Column('activity', String),
    Column('massuser', String),
    Column('auth', Boolean, default=ColumnDefault(False)),
    Column('train', Integer, default=ColumnDefault(1)),
    Column('kkal', Integer, default=ColumnDefault(0)),
    Column('belki', Integer, default=ColumnDefault(0)),
    Column('jiry', Integer, default=ColumnDefault(0)),
    Column('ugli', Integer, default=ColumnDefault(0)),
    Column('day_train', Integer, default=ColumnDefault(1)),
    Column('registration_date', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['registration_date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['registration_date'].drop()
