from zone_common.events.base_publisher import Publisher
from zone_common.events.subjects import Subjects


class ProductCreatedPublisher(Publisher):
    subject = Subjects.ProductCreated

    def __init__(self, client):
        super().__init__(client=client)
