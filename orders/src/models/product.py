from sqlalchemy import INTEGER, Column, String, event, FLOAT
from nanoid import generate

from .base import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(INTEGER(), primary_key=True)
    uuid = Column(String(), nullable=False)
    title = Column(String(), nullable=False)
    price = Column(FLOAT(), nullable=False)
    description = Column(String(), nullable=False)
    versionId = Column(INTEGER(), nullable=False)

    __mapper_args__ = {"version_id_col": versionId}
