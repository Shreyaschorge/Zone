from sqlalchemy import Column, String, INTEGER, event, Table, ForeignKey, FLOAT
from sqlalchemy.orm import relationship
from nanoid import generate

from schema.product import ProductSchema
from .product import Product
from .base import Base

product_schema = ProductSchema(many=True)

order_product = Table("order_product", Base.metadata,
                      Column("orderId", ForeignKey("orders.uuid")),
                      Column("productId", ForeignKey("products.uuid"))
                      )


class Order(Base):
    __tablename__ = "orders"
    id = Column(INTEGER(), primary_key=True)
    uuid = Column(String(), nullable=False)
    versionId = Column(INTEGER(), nullable=False)

    products = relationship(
        "Product", secondary=order_product, backref='orders')

    __mapper_args__ = {"version_id_col": versionId}

    def to_dict(self):
        return {"uuid": self.uuid, "products": product_schema.dump(self.products)}


def add_uuid(mapper, connect, target):
    target.uuid = f'order_{generate(size=30)}'


event.listen(Order, 'before_insert', add_uuid)
