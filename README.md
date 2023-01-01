## Zone

Zone a C2C platform, build with scalability and availability in mind.

Zone uses a custom utility library [zone-common](https://pypi.org/project/zone-common/). Github: [zone-common](https://github.com/Shreyaschorge/zone_common)

### Architecture

<img src="snapshots/zone-arch.jpeg"/>

This application is divided into 5 micro-services.

1. Authentication

   1. Password Encryption: [Argon2](https://en.wikipedia.org/wiki/Argon2).
   2. Mechanism: [JWT](https://jwt.io/).
   3. Pattern: Access and refresh tokens.

2. Products

   1. Create, Fetch and Update Products.

3. Orders

   1. Create, Update Orders

4. Payments

   1. Create Payments

5. Client

   1. Provides UI to end users to interact with the app.

Messaging System used to communicate between these services is [NATS](https://nats.io/).

Messages are persisted using [NATS-Jetstream].

The zone has 3 streams that persist messages.

    1. products
    2. orders
    3. payments

[Example of NATS](https://docs.nats.io/nats-concepts/jetstream/consumers/example_configuration)

Events/messages flowing in the application:

    1. PRODUCT.created
    2. PRODUCT.updated
    3. ORDER.created
    4. ORDER.cancelled
    5. PAYMENT.created

[Queue Groups](https://docs.nats.io/nats-concepts/core-nats/queue)

Type of QueueGroups in the application

    1. product_created_listeners
    2. product_updated_listeners
    3. payment_created_listeners
    4. order_created_listeners
    5. order_cancelled_listeners

All Listeners/Consumers are of type [Queue Push Consumers.](https://natsbyexample.com/examples/jetstream/queue-push-consumer/)

###UI Demo.

https://www.loom.com/share/40319d495c8d4bae9639012b0ef93b9c
