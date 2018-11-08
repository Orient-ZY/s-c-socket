# -*- coding: UTF-8 -*-
import time
import sys
import RPi.GPIO as GPIO
import picamera
import os
import socket


def get_time():
	datetime = time.strftime('%Y-%m-%d_%H_%M_%S',time.localtime(time.time()))
	return datetime

def get_image(datetime):
    camera = picamera.PiCamera()
    image_name = datetime + ".jpg"
    camera.start_preview()
    camera.resolution = (1024,768)
    camera.capture(image_name)
    camera.close()

    return image_name

def client(image_name):
    path = os.path.join('./', image_name)
    file_name = os.path.basename(path)
    file_size = os.stat(path).st_size
    file_info = "%s|%s" % (file_name,file_size)
    c.sendall(bytes(file_info))
    has_sent = 0
    with open(path, 'rb') as fp:
        while has_sent != file_size:
            data = fp.read(1024)
            c.sendall(data)
            has_sent += len(data)
            print '\r' + '[上传进度]:%s%.02f%%' % ('>' * int((has_sent / file_size) * 50), float(has_sent / file_size) * 100),
    print ''
    print '%s上传成功!'% file_name


if __name__ == '__main__':

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12,GPIO.IN)

    IP_PORT = ('134.175.54.53', 8888)
    c = socket.socket()
    c.connect(IP_PORT)

    try:
        while 1:
            if GPIO.input(12) == 0:
                try:
                    date_time = get_time()
                    image_name = get_image(date_time)
                    client(image_name)
                except Exception as e:
                    print "something wrong!!!"
                    print e
                time.sleep(5)
            else:
                continue
    except KeyboardInterrupt:
        c.close()
        GPIO.cleanup()
        sys.exit(-1)
