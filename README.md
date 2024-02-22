# Home Assistant

## Requirements

### Hardware

- BME280 or BME680 Sensors
- Raspberry Pi 3+/4/5, Raspberry Pi Zero 2W

### Software

- Python 3.9+
- Docker (Optional)

### Setup

```sh
# Create virtual environment
python3 -m venv venv
# Activate it
source ./venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

### Create database

You must run the [create](./db/create.sql) file in the database to create the necessary tables.

## Create cronjob

```sh
sudo crontab -e

# add the following
*/5 * * * * cd <path to project>; ./cron.sh >> /var/log/cronlogs.log 2>&1
```

## Run the API with Uvicorn

```sh
# Run uvicorn against 0.0.0.0, so it can be accessible to other machines
uvicorn main:app --reload --host=0.0.0.0
```

Once it's running just go to the IP address of the server with the port `8000`, example: http://192.168.0.100:8000.

If you don't know the IP of the server, you can simply run the following command from the machine:

```sh
hostname -I
```

## Run it as a service with Supervisord

Run the uvicorn server with `supervisord`:

```sh
supervisord

# Or run it in foreground
supervisord -n
```

Then to stop it:

```sh
pkill -f supervisord
```

## Run it with Docker

Build the image:

```sh
docker build -t raspi-temp .
```

Run the container:

```sh
docker run --rm -d --name raspi-temp -p 8000:8000 raspi-temp
```

Stop the container:

```sh
docker stop raspi-temp
```