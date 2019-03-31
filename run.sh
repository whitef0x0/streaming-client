#!/bin/bash
python start.py && ffmpeg -loglevel error -f avfoundation -framerate 30 -pix_fmt 0rgb -i 0 -vcodec libx264  -preset ultrafast -tune zerolatency -thread_type slice -slices 1 -intra-refresh 1 -r 30 -g 60 -s 640x480 -aspect 4:3 -acodec aac -ar 44100 -b:v 2.6M -minrate:v 900k -maxrate:v 1.5M -bufsize:v 1M -b:a 128K -f mpegts udp://0.0.0.0:8080?pkt_size=1316

