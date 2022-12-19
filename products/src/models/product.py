from sqlalchemy import INTEGER, Column, String, event, FLOAT
from sqlalchemy.orm import declarative_base
from nanoid import generate

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(INTEGER(), primary_key=True)
    uuid = Column(String(), nullable=False)
    title = Column(String(), nullable=False)
    price = Column(FLOAT(), nullable=False)
    description = Column(String(), nullable=False)
    userId = Column(String())
    version_id = Column(INTEGER(), nullable=False)

    __mapper_args__ = {"version_id_col": version_id}


def add_uuid(mapper, connect, target):
    target.uuid = f'product_{generate(size=30)}'


event.listen(Product, 'before_insert', add_uuid)
