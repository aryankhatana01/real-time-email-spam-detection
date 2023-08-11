#!/bin/bash

# Run test.sh and wait for it to finish
./wait-for-it.sh kafka:9092

python3 /app/create_topics.py

# Navigate to the directory of script1.py and run it in the background
cd /app/computation
python3 consume.py &

# Navigate to the directory of script2.py and run it in the background
cd /app/delete_spam
python3 delete_spam.py &

# Navigate to the directory of script3.py and run it in the background
cd /app/ingestion
python3 produce.py &

# Wait for all background processes to complete before exiting
wait