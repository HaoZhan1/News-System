#!/bin/bash
redis-server
brew services start mongodb

cd back-end/recommendation_service
python click_log_process.py &
python recommendation_service.py &

cd ..
python service.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES" PRESSKEY

kill $(jobs -p)
