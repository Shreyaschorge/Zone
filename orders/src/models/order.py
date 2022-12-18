from sqlalchemy import Column, String, INTEGER, event
from sqlalchemy.orm import declarative_base
from nanoid import generate

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    id = Column(INTEGER(), primary_key=True)
    uuid = Column(String(), nullable=False)
    productId = Column(String(), nullable=False)
    versionId = Column(INTEGER(), nullable=False)

    __mapper_args__ = {"version_id_col": versionId}

    def to_json(self):
        return {"orderId": self.uuid, "productId": self.productId}


def add_uuid(mapper, connect, target):
    target.uuid = f'order_{generate(size=30)}'


event.listen(Order, 'before_insert', add_uuid)
