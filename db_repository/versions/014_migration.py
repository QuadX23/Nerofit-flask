from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
exercises = Table('exercises', post_meta,
    Column('exercise_id', Integer, primary_key=True, nullable=False),
    Column('training_id', Integer, primary_key=True, nullable=False),
)

training_exercise = Table('training_exercise', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String),
    Column('video', Integer, nullable=False),
)

training_video = Table('training_video', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('url', String),
    Column('description', String),
)

training = Table('training', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('day', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['exercises'].create()
    post_meta.tables['training_exercise'].create()
    post_meta.tables['training_video'].create()
    post_meta.tables['training'].columns['day'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['exercises'].drop()
    post_meta.tables['training_exercise'].drop()
    post_meta.tables['training_video'].drop()
    post_meta.tables['training'].columns['day'].drop()
