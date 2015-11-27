# showbaby
A simple baby monitor with GUI for raspberry pi

## Installation
[values in brackets should be double checked and changed]

### Raspberry pi setup

I personally prefer [minibian](https://minibianpi.wordpress.com/), but it should work with any raspberry distro of your choice.
Make sure that ssh-keys are ok and you are able to login into your vps from raspberry without password.

### Motion setup

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
webcam_port 8081
webcam_localhost off
```

### Python env setup

```
sudo apt-get install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Nginx and uwsgi
```
sudo apt-get install nginx
# Mind that home directory path should be updated.
sudo cp sample_nginx.conf /etc/nginx/sites-available/showbaby.conf
sudo ln -s /etc/nginx/sites-available/showbaby.conf /etc/nginx/sites-enabled/showbaby.conf
```
uwsgi has already been installed directly to .venv. Modify uwsgi.ini:
```
base = /home/ina/projects [path to src parent directory]
logto = %(base)/logs/%(project)_uwsgi.log [path to uwsgi logs]
```

### VPS streaming setup
Install autossh

```
sudo apt-get install autossh
```

Set proper parameters in config.py
```
# vps user
REMOTE_USER = "ina" [your vps user]
# vps port to stream
REMOTE_PORT = 9000
# motion webcam_port
LOCAL_PORT = 8081
# rasberry pi ip
LOCAL_IP = "192.168.0.30"
# vps ip
REMOTE_IP = "95.85.51.79" [your vps ip]
```

### Autostart

Make uwsgi start on boot
```
crontab -l | { cat; echo "@reboot /home/ina/projects/showbaby/.venv/bin/uwsgi --ini /home/ina/projects/showbaby/uwsgi.ini"; } | crontab -
```
###

Voila, reaching your raspberry pi's ip in browser shows you the GUI to control streaming to the outside world! :)

## TODO
- [ ] ansible job for autoinstall
- [ ] android widget for streaming control
