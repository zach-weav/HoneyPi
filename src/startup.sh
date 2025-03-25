#!/bin/bash

echo "=== Starting Honeypot Containers ==="

sleep 2

echo "Make sure docker is running..."
sudo systemctl start docker

# Check if any process is using port 3306 and kill it if necessary
echo "Checking if any process is using port 3306..."
pid=$(sudo lsof -t -i:3306)

if [ -n "$pid" ]; then
    echo "Port 3306 is occupied by process with PID: $pid. Killing the process..."
    sudo kill -9 $pid
    sleep 2  # Give it some time to fully kill the process
else
    echo "No process found using port 3306."
fi

# Now start the MySQL container
echo "Starting mysql container..."
docker start mysql_honeypot

# Start the other containers
echo "Starting ssh container..."
docker start ssh_honeypot

echo "Starting loki container..."
docker start loki

echo "Starting promtail container..."
docker start promtail

echo "Starting grafana container..."
docker start grafana

echo "Starting prometheus"
docker start prometheus

echo "Starting cadvisor"
docker start cadvisor

echo "=== Honeypot Setup Complete ==="
