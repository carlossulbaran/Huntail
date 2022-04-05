#!/usr/bin/env python

from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()
sleep(5)
camera.capture('picture3.jpg')
camera.stop_preview()
