#!/bin/bash

case "$1" in
    up)
        docker compose -f docker-compose.yml -f docker-compose.prod.yml up
        ;;
    down)
        docker compose -f docker-compose.yml -f docker-compose.prod.yml down
        ;;
    build)
        docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
        ;;
    *)
        echo "Usage: $0 {up|down|build}"
        exit 1
        ;;
esac