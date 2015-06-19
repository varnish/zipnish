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

# Process Order (Parallel: Fetch Customer / Fetch Products)
node app.js --port 5000 --address 127.0.0.1 --service 'Process Order' --flow parallel --call http://127.0.0.1:5005/ &

# Fetch Customer
node app.js --port 5005 --address 127.0.0.1 --service 'Fetch Customer' &

# Fetch Products
node app.js --port 5010 --address 127.0.0.1 --service 'Fetch Products' &
node app.js --port 5011 --address 127.0.0.1 --service 'Fetch Product' &


# Get Payment Information
node app.js --port 5020 --address 127.0.0.1 --service 'Get Payment Information' &

# Validate Credit Card
node app.js --port 5021 --address 127.0.0.1 --service 'Validate Credit Card' &
node app.js --port 5022 --address 127.0.0.1 --service 'Verify Credit Card' &

# Approve Payment
node app.js --port 5031 --address 127.0.0.1 --service 'Approve Payment' &


# PARALLEL

# Update Inventory
node app.js --port 5051 --address 127.0.0.1 --service 'Update Inventory' &

# Update Order Status
node app.js --port 5052 --address 127.0.0.1 --service 'Update Order Status' &

# Send Order Email
node app.js --port 5053 --address 127.0.0.1 --service 'Send Order Email' &

# Update Order Shipping Status
node app.js --port 5053 --address 127.0.0.1 --service 'Update Order Shipping Status' &

exit
