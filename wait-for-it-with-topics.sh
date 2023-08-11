#!/bin/bash
# wait-for-it.sh: Wait for a service and topics to be ready

# Usage: ./wait-for-it.sh host:port topic1 topic2 [-- command args]
#    or ./wait-for-it.sh host:port topic1 topic2 [-s] [-- command args]
#    -s: Strict mode: exit if the host or topic is unavailable

set -e

hostport=$1
shift
topics=("$@")
cmd=

if [ "${topics[0]}" = "-s" ]; then
    strict_mode=1
    shift
    topics=("${topics[@]:1}")
fi

cmd=${topics[-1]} # Last element is the command to execute
unset 'topics[${#topics[@]}-1]' # Remove the last element

host=$(echo $hostport | cut -d':' -f1)
port=$(echo $hostport | cut -d':' -f2)

echo "Waiting for $host:$port to be ready..."

for i in {1..30}; do
    if python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(2); s.connect(('${host}', ${port}));"; then
        echo "$host:$port is available!"
        
        # Check if topics are available
        topics_available=1
        for topic in "${topics[@]}"; do
            if ! /kafka-3.5.1-src/bin/kafka-topics.sh --describe --topic "$topic" --bootstrap-server "$host:$port"; then
                topics_available=0
                break
            fi
        done
        
        if [ "$topics_available" -eq 1 ]; then
            echo "Kafka topics are available!"
            if [ ! -z "$cmd" ]; then
                exec $cmd
            fi
            exit 0
        else
            echo "Kafka topics are not yet available."
        fi
    fi
    sleep 1
done

echo "Timeout reached, $host:$port or Kafka topics are still unavailable."

if [ "$strict_mode" = "1" ]; then
    exit 1
fi
