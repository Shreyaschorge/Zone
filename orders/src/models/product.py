from sqlalchemy import INTEGER, Column, String, FLOAT
from sqlalchemy.orm import relationship

from .base import Base
from schema.order import OrderSchema

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
        "Order", secondary="order_products", back_populates='products')

    order_products = relationship(
        "OrderProduct", back_populates="product")

    def to_dict(self):
        return {"uuid": self.uuid, "title": self.title, "price": self.price, "description": self.description, "userId": self.userId, "orders": order_schema.dump(self.orders)}

    __mapper_args__ = {"version_id_col": version_id}
