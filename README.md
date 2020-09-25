# audioStreamer

# Installation

    sudo apt install python3-flask
    sudo cp audioStreamer.service /etc/systemd/system/audioStreamer.service
    sudo systemctl daemon-reload
    sudo systemctl restart audioStreamer.service

# Commands

### /start (POST)

Provide an IP in the 'IP' field. For example:

    curl localhost:5000/start -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "IP=192.168.0.1"

### /status (GET)

Tells you if ffplay is still running or not.

### /wake (GET)

Wake up screen. Helpful if screensaver was activated. Simply sends a keypress.
