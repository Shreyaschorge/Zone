from sqlalchemy import Column, String, INTEGER, event, Table, ForeignKey, FLOAT
from sqlalchemy.orm import relationship
from nanoid import generate
from zone_common.events.order_status import OrderStatus

from schema.product import ProductSchema
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
    userId = Column(String(), nullable=False)
    status = Column(String(), nullable=False, default=OrderStatus.Draft)
    version_id = Column(INTEGER(), nullable=False)

    products = relationship(
        "Product", secondary=order_product, back_populates='orders')

    __mapper_args__ = {"version_id_col": version_id}

    def to_dict(self):
        return {"uuid": self.uuid, "userId": self.userId, "products": product_schema.dump(self.products)}


def add_uuid(mapper, connect, target):
    target.uuid = f'order_{generate(size=30)}'


event.listen(Order, 'before_insert', add_uuid)
