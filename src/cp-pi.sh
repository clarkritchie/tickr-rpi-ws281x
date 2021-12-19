#!/usr/bin/env bash
PI_ADDRESS=${1:-192.168.7.105}
scp *sh pi@${PI_ADDRESS}:~/tmp
scp *py pi@${PI_ADDRESS}:~/tmp
scp requirements.txt pi@${PI_ADDRESS}:~/tmp