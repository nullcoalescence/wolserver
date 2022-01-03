# wolserver
## A wake-on-lan server written in Python

## About
This application spins up a webserver that allows you to save device's mac addresses to a SQLITE database, and wake them up either from a UI or from hitting a endpoint on your local network. I personally run this on my Raspberry PI, so when I remote into my network I can easily access the web page and send wake-up commands to my devices.

## Build instructions
```
# Install pre-reqs
$ sudo apt install python3 git

# Download and build
$ git clone https://github.com/benDotDirectory/wolserver.git ~/wolserver
$ cd ~/wolserver
$ pip3 install -r requirements.txt

# Run
# Linux:
$ ./start.sh
# Windows:
$ ./start.ps1

# Run with task scheduler (Ex. PM2)
$ npm install -g pm2
$ pm2 start ~/wolserver/server.py --name "wolserver" --interpreter "python3"
```

## Send HTTP requests to devices
@TODO
