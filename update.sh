#!/bin/bash

docker stop raspi-temp

docker rm raspi-temp

docker build -t raspi-temp .

docker run --name raspi-temp -d -p 8000:8000 --restart unless-stopped raspi-temp