from zone_common.events.base_publisher import Publisher
from zone_common.events.subjects import Subjects


class PaymentCreatedPublisher(Publisher):
    subject = Subjects.PaymentCreated

    def __init__(self, client):
        super().__init__(client=client)
