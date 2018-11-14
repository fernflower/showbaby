# showbaby
A simple baby monitor with GUI for raspberry pi

## Installation
Added docker files for customizing and launching motion on ubuntu and rpi-rasbian [wip].
Docker images don't include nginx/uwsgi/flask for having additional webui with 2 stream control buttons
(to be honest getting back to this project 2 years from initial commit makes in look like an overkill).
```
docker build -f docker/Dockerfile_ubuntu -t motion .
docker run -p 8081:8081 -p 8080:8080 --device /dev/video0:/dev/video0 -v /home/ina/showbaby_data/prague:/var/lib/motion --privileged -dt motion
```

### Raspberry pi setup
Tested on [raspbian stretch lite](https://www.raspberrypi.org/downloads/raspbian/) 2018-10-19.

### (deprecated) Non-docker motion setup

Popular motion detector library which works out of the box [Motion](http://www.lavrsen.dk/foswiki/bin/view/Motion/WebHome).

```
sudo apt-get install motion
```
Optional v4l2-ctl install, handy for video device number and webcam resolution retrieval.
```
sudo apt-get install v4l-utils
```
Change several parameters in /etc/motion/motion.conf:

```
daemon on
# v4l2-ctl --list-devices
videodevice /dev/video0 
# v4l2-ctl --list-formats and v4l2-ctl --list-framesizes=YUYV [your format here]
width 640
height 320
# up to ypur choice
framerate 15
# don't save images
output_all off
target_dir /home/ina/showbaby [your directory to store filmed videos]
stream_port 8081
# enable streaming outside localhost
stream_localhost off
```

Now you can connect rpi and iphone\android phone via [zerotier](https://www.zerotier.com) subnet and have 24\7 fun :) 
