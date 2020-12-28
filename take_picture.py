from picamera import PiCamera
import numpy as np
import time
import argparse
import os
import threading
import csv

from UWB import UWB

def write_csv(root, data):
    csv_path = os.path.join(root, 'trajectory-{}.csv'.format(args.number))
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['D1', 'D2', 'D3', 'rX', 'rY', 'gX', 'gY'])
        for d in data:
            writer.writerow(d)
    print("Write csv done.")

parser = argparse.ArgumentParser()
parser.add_argument('--number', required=True, type=int)

args = parser.parse_args()
folder = os.path.join('data', str(args.number))
if not os.path.isdir(folder):
    os.makedirs(folder)

# Configure UWB
print("Configuring UWB...")
uwb = UWB()
t = threading.Thread(target=uwb.distance, daemon=True)
t.start()

# Configure PiCamera setting
print("Configuring PiCamera...")
camera = PiCamera(resolution=(720, 720), framerate=30)
# Set ISO to the desired value
camera.iso = 400
camera.brightness = 50
# Wait for the automatic gain control to settle
time.sleep(2)
# Now fix the values
camera.shutter_speed = 12000

camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

input("Press Enter to continue...")
data_num = 7
data = [None for i in range(data_num)]
prev_d1, d2, d3 = uwb.get_distance()
number = 0
while True:
    d1, d2, d3 = uwb.get_distance()
    if d1 != prev_d1:
        rx, ry = uwb.triposition()
        print("[number: {}] D1: {}, D2: {}, D3: {}, Position: {}".format(number, d1, d2, d3, (rx, ry)))
        data[number] = [d1, d2, d3, rx, ry]

        filename = os.path.join(folder, 'image-{}.png'.format(number))
        camera.capture(filename)

        prev_d1 = d1
        number += 1

    if number == data_num:
        break
write_csv(folder, data)
uwb.end()
camera.close()
