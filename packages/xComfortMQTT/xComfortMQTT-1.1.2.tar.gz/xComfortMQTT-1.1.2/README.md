# xComfortMQTT

[![Travis](https://travis-ci.org/blavka/xComfortMQTT.svg?branch=master)](https://travis-ci.org/blavka/xComfortMQTT)
[![Release](https://img.shields.io/github/release/blavka/xComfortMQTT.svg)](https://github.com/blavka/xComfortMQTT/releases)
[![License](https://img.shields.io/github/license/blavka/xComfortMQTT.svg)](https://github.com/blavka/xComfortMQTT/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/xComfortMQTT.svg)](https://pypi.org/project/xComfortMQTT)

## Installing

You can install **xComfortMQTT** directly from PyPI:

```sh
sudo pip3 install -U xComfortMQTT
```

## Config

Insert this snippet to the file /etc/xComfortMQTT.yml:
```yml
---
shc:
  host: 192.168.0.2
  username: admin
  password: very-strong-password

mqtt:
  host: 192.168.0.1
```

## Usage

Update /etc/xComfortMQTT.yml and run

```sh
xComfortMQTT -c /etc/xComfortMQTT.yml
```

## Systemd

Insert this snippet to the file /etc/systemd/system/xComfortMQTT.service:
```
[Unit]
Description=xComfortMQTT
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/xComfortMQTT -c /etc/xComfortMQTT.yml
Restart=always
RestartSec=5
StartLimitIntervalSec=0

[Install]
WantedBy=multi-user.target
```

Enable the service start on boot:
```sh
sudo systemctl enable xComfortMQTT.service
```

Start the service:

```sh
sudo systemctl start xComfortMQTT.service
```

View the service log:
```sh
journalctl -u xComfortMQTT.service -f
```

## PM2

```sh
pm2 start /usr/bin/python3 --name "xComfortMQTT" -- /usr/local/bin/xComfortMQTT -c /etc/xComfortMQTT.yml
pm2 save
```

## Development
```
git clone git@github.com:blavka/xComfortMQTT.git
cd xComfortMQTT
./test.sh
sudo python3 setup.py develop
```
