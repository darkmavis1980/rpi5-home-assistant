# Home Assistant

## Requirements

### Hardware

- BME280 Sensor
- Raspberry Pi 3+/4/5

### Software

- Python 3.9+

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



## Create cronjob

```sh
sudo crontab -e

# add the following
*/5 * * * * cd <path to project>; ./cron.sh >> /var/log/cronlogs.log 2>&1
```

## Run the API

```sh
# Run uvicorn against 0.0.0.0, so it can be accessible to other machines
uvicorn main:app --reload --host=0.0.0.0
```

Once it's running just go to the IP address of the server with the port `8000`, example: http://192.168.0.100:8000.

If you don't know the IP of the server, you can simply run the following command from the machine:

```sh
hostname -I
```

## Run it as a service

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