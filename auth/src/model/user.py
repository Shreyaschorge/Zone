from db import db
from nanoid import generate


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


@db.event.listens_for(UserModel, 'before_insert')
def add_uuid(mapper, connect, target):
    target.uuid = f'user_{generate(size=20)}'
