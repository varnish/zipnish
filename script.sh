#!/bin/bash

# terminate any existing node web services
kill $(ps au | grep node | grep -v 'grep' | awk '{print $2}')

if [ $terminate ]
then
  exit
fi

# Process Order
node app.js --port 5000 --address 127.0.0.1 --service 'Process Order'

