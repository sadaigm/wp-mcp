#!/bin/bash
echo "Building Docker image: wp-mcp:latest..."
docker build -t wp-mcp:latest .
echo "Build complete."