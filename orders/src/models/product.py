from sqlalchemy import INTEGER, Column, String, event, FLOAT
from nanoid import generate
from sqlalchemy.orm import relationship

from .base import Base
from schema.order import OrderSchema
from models.order import order_product

order_schema = OrderSchema(many=True)


class Product(Base):
    __tablename__ = "products"
    uuid = Column(String(), primary_key=True)
    title = Column(String(), nullable=False)
    price = Column(FLOAT(), nullable=False)
    description = Column(String(), nullable=False)
    userId = Column(String(), nullable=False)
    version_id = Column(INTEGER(), nullable=False)

    orders = relationship(
        "Order", secondary=order_product, back_populates='products')

    def to_dict(self):
        return {"uuid": self.uuid, "title": self.title, "price": self.price, "description": self.description, "userId": self.userId, "orders": order_schema.dump(self.orders)}

    __mapper_args__ = {"version_id_col": version_id}
