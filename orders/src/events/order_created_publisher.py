from zone_common.events.base_publisher import Publisher
from zone_common.events.subjects import Subjects


class OrderCreatedPublisher(Publisher):
    subject = Subjects.OrderCreated

    def __init__(self, client):
        super().__init__(client=client)
