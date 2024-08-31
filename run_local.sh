#!/bin/bash

# Load environment variables from the .env file
if [ -f .env ]; then
  export $(cat .env | xargs)
else
  echo ".env file not found. Please create a .env file with the necessary environment variables."
  exit 1
fi

# Start with a base port
BASE_PORT=6970
PORT=$BASE_PORT

# Function to check if a port is in use
function is_port_in_use() {
  if lsof -i:$1 > /dev/null; then
    return 0  # Port is in use
  else
    return 1  # Port is not in use
  fi
}

# Find an available port
while is_port_in_use $PORT; do
  echo "Port $PORT is in use, trying next port..."
  PORT=$((PORT + 1))
done

echo "Using port $PORT"

# Build the Docker image
sudo docker buildx build --platform linux/amd64 -t data-analyst .


# Run the Docker container with the environment variables and the available port
docker run --platform linux/amd64 -d -p $PORT:8080 \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -e GROQ_API_KEY="$GROQ_API_KEY" \
  data-analyst

echo "Docker container is running and accessible at http://localhost:$PORT"