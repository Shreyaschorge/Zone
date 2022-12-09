from db import db
from nanoid import generate


class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    userId = db.Column(db.String)
    orderId = db.Column(db.String)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def find_user_products(cls, userUuid):
        return cls.query.filter_by(userId=userUuid).all()


@db.event.listens_for(ProductModel, 'before_insert')
def add_uuid(mapper, connect, target):
    target.uuid = f'product_{generate(size=30)}'
