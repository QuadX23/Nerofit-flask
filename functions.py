from sqlalchemy import MetaData, Table
from app import db


def user_add(class_name, username, password):
    user = class_name(username=username, password=password)
    db.session.add(user)
    db.session.commit()

# def user_delete(id):
#     db_session.query(User). \
#         filter(User.id == id). \
#         delete()
#     db_session.commit()
#
# def gender_user_by_id(id, gender):
#     user = User.query.get(id)
#     user.gender = gender
#     db_session.commit()