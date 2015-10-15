#!/bin/bash

# terminate any existing node web services
NODE_SERVICES=$(ps au | grep node | grep -v 'grep' | awk '{print $2}')

if [ ! -z "$NODE_SERVICES" ]
then
  kill $NODE_SERVICES
fi

if [ $terminate ]
then
  exit
fi


# Change directory to rpc-service/
cd rpc-service

node app.js --port 9000 --proxy-port 6081 --address 192.168.33.14 --service 'Process Order' \
            --services '/process-order:Process Order=>serial:/fetch-customer,/fetch-products,/get-payment-information' \
            --services '/fetch-customer:Fetch Customer' \
            --services '/fetch-products:Fetch Products=>serial:/fetch-product' \
            --services '/fetch-product:Fetch Product' \
            --services '/get-payment-information:Get Payment Information=>serial:/validate-credit-card,/verify-credit-card' \
            --services '/validate-credit-card:Validate Credit Card' \
            --services '/verify-credit-card:Verify Credit Card=>serial:/approve-payment' \
            --services '/approve-payment:Approve Payment=>parallel:/update-inventory,/update-order-status,/send-order-email,/update-order-shipping-status' \
            --services '/update-inventory:Update Inventory' \
            --services '/update-order-status:Update Order Status' \
            --services '/send-order-email:Send Order Email' \
            --services '/update-order-shipping-status:Update Order Shipping Status' \
exit
