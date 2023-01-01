from sqlalchemy import INTEGER, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class OrderProduct(Base):
    __tablename__ = "order_products"
    id = Column(Integer, primary_key=True)
    orderId = Column(String, ForeignKey("orders.uuid"))
    productId = Column(String, ForeignKey("products.uuid"))
    quantity = Column(Integer)

    # Define the relationships to the Order and Product tables
    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")
