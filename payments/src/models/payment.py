from sqlalchemy import Column, String, Float, ForeignKey, event
from sqlalchemy.orm import relationship

from .base import Base


class Payment(Base):
    __tablename__ = "payments"
    uuid = Column(String(), primary_key=True)
    orderId = Column(String(), ForeignKey("orders.uuid"))
    chargeId = Column(String(), nullable=False)

    order = relationship("Order", back_populates="payment")


def add_uuid(mapper, connect, target):
    target.uuid = f'payment_{generate(size=30)}'


event.listen(Payment, 'before_insert', add_uuid)
