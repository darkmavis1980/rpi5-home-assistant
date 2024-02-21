#!/bin/bash

docker stop raspi-temp

docker build -t raspi-temp .

docker run --name raspi-temp --rm -d -p 8000:8000 raspi-temp