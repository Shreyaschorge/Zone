from sqlalchemy import Column, String, INTEGER, event, Table, ForeignKey, FLOAT, Integer
from sqlalchemy.orm import relationship
from nanoid import generate
from zone_common.events.order_status import OrderStatus

from schema.product import ProductSchema
from .base import Base

product_schema = ProductSchema(many=True)


class Order(Base):
    __tablename__ = "orders"
    uuid = Column(String(), primary_key=True)
    userId = Column(String(), nullable=False)
    status = Column(String(), nullable=False, default=OrderStatus.Draft)
    version_id = Column(INTEGER(), nullable=False)

    products = relationship(
        "Product", secondary="order_products", back_populates='orders')

    order_products = relationship(
        "OrderProduct", back_populates="order")

    __mapper_args__ = {"version_id_col": version_id}

    def to_dict(self):
        return {"uuid": self.uuid, "userId": self.userId, "status": self.status, "products": [{
            "title": product.title,
            "price": product.price,
            "description": product.description,
            "uuid": product.uuid,
            "userId": product.userId,
            "quantity": product.order_products.quantity
        } for product in self.products]}


def add_uuid(mapper, connect, target):
    target.uuid = f'order_{generate(size=30)}'


event.listen(Order, 'before_insert', add_uuid)
