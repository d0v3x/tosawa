from picamera import PiCamera
from time import sleep
from datetime import datetime

camera = PiCamera()

camera.resolution = (1024, 1024)

camera.start_preview(alpha=200)

for i in range(60):
    sleep(3)
    current_time = datetime.now().strftime('%H%M%S')
    camera.capture('/home/pi/ai101/A/image_%s.jpg' % current_time)

camera.stop_preview()
