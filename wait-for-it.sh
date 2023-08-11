#!/bin/bash
# wait-for-it.sh: Wait for a service to be ready

# Usage: ./wait-for-it.sh host:port [-- command args]
#    or ./wait-for-it.sh host:port [-s] [-- command args]
#    -s: Strict mode: exit if the host is unavailable

set -e

hostport=$1
shift
cmd=$@

if [ "$1" = "-s" ]; then
    strict_mode=1
    shift
fi

host=$(echo $hostport | cut -d':' -f1)
port=$(echo $hostport | cut -d':' -f2)

echo "Waiting for $host:$port to be ready..."

for i in {1..30}; do
    if nc -z $host $port; then
        echo "$host:$port is available!"
        if [ ! -z "$cmd" ]; then
            exec $cmd
        fi
        exit 0
    fi
    sleep 3
done

echo "Timeout reached, $host:$port is still unavailable."

if [ "$strict_mode" = "1" ]; then
    exit 1
fi
