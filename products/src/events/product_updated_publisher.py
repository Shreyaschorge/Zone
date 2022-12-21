from zone_common.events.base_publisher import Publisher
from zone_common.events.subjects import Subjects
from nats.aio.client import Client as NATS


class ProductUpdatedPublisher(Publisher):
    subject = Subjects.ProductUpdated

    def __init__(self, client):
        super().__init__(client=client)
