#!/bin/bash

# terminate any existing node web services
kill $(ps au | grep node | grep -v 'grep' | awk '{print $2}')

if [ $terminate ]
then
  exit
fi

# Process Order
node app.js --port 5000 --address 127.0.0.1 --service 'Process Order'


# Fetch Customer
node app.js --port 5010 --address 127.0.0.1 --service 'Fetch Customer'

# Fetch Product
node app.js --port 5011 --address 127.0.0.1 --service 'Fetch Product'


# Get Payment Information
node app.js --port 5020 --address 127.0.0.1 --service 'Get Payment Information'

# Validate Credit Card
node app.js --port 5021 --address 127.0.0.1 --service 'Validate Credit Card'
node app.js --port 5022 --address 127.0.0.1 --service 'Verify Credit Card'
