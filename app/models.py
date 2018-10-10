from datetime import datetime

from flask_login import UserMixin

from app import db

AUTH_FALSE = False
AUTH_TRUE = True


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(120))
    gender = db.Column(db.String)
    data = db.Column(db.String)
    height = db.Column(db.String)
    activity = db.Column(db.String)
    massuser = db.Column(db.String)
    auth = db.Column(db.Boolean, default=AUTH_FALSE)
    train = db.Column(db.Integer, default=1)
    kkal = db.Column(db.Integer, default=0)
    belki = db.Column(db.Integer, default=0)
    jiry = db.Column(db.Integer, default=0)
    ugli = db.Column(db.Integer, default=0)
    day_train = db.Column(db.Integer, default=1)
    registration_date = db.Column(db.DateTime, default=datetime.now)

    user_info = db.relationship('user_info', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        pass

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class user_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mass = db.Column(db.String)
    chest = db.Column(db.String)
    body = db.Column(db.String)
    left_hand = db.Column(db.String)
    left_bedro = db.Column(db.String)
    left_golen = db.Column(db.String)
    waist = db.Column(db.String)
    buttock = db.Column(db.String)
    right_hand = db.Column(db.String)
    right_bedro = db.Column(db.String)
    right_golen = db.Column(db.String)
    # timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id_helper = db.Column(db.Integer)

    def __repr__(self):
        return '<user_info %r>' % self.mass


class TrainingVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return '<TrainVideo %r>' % self.name


exercises = db.Table(
    'exercises',
    db.Column('exercise_id', db.Integer, db.ForeignKey('training_exercise.id'), primary_key=True),
    db.Column('training_id', db.Integer, db.ForeignKey('training.id'), primary_key=True)
)


class TrainingExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String)
    video_id = db.Column(db.Integer, db.ForeignKey(TrainingVideo.id), nullable=False)

    video = db.relationship('TrainingVideo')


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    exercises = db.relationship(
        'TrainingExercise',
        secondary=exercises,
        lazy='subquery',
        backref=db.backref('trainings', lazy=True)
    )

    def __repr__(self):
        return '<TrainVideo %r>' % self.name
