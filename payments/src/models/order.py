from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship

from .base import Base


class Order(Base):
    __tablename__ = "orders"
    uuid = Column(String(), primary_key=True)
    price = Column(Float(), nullable=False)
    userId = Column(String(), nullable=False)
    status = Column(String(), nullable=False)
    version_id = Column(Integer(), nullable=False)

    payment = relationship("Payment", uselist=False, back_populates="order")

    __mapper_args__ = {"version_id_col": version_id}
