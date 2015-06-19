Here we describe an example of a set of services which can be created using the [``following``](RPC Services.md).

If ``--flow series`` is specified, each step will finish before moving to the next step.

***Process Order***

Steps below proceed in ``series``.

1. Fetch Customer
2. Fetch Products
  1. Fetch Product
3. Fetch Payment Information
  1. Validate Credit Card
    2. Verify Credit Card
4. Approve Payment

Steps below proceed in ``parallel``.

* Update Inventory
* Update Order Status
* Send Order Email
* Update Order Shipping Status
