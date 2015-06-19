Here we describe an example of a set of services which can be created using the [following](RPC Services.md).

To see how the flow of request take place. Please refer to the [bash script](../script.sh)

***Process Order***

1. Fetch Customer
2. Fetch Products
  1. Fetch Product
3. Fetch Payment Information
  1. Validate Credit Card
    2. Verify Credit Card
4. Approve Payment


* Update Inventory
* Update Order Status
* Send Order Email
* Update Order Shipping Status
