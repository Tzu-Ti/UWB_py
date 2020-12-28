import serial
import time
import numpy as np
import sympy
import threading

class UWB():
  def __init__(self):
    self.DWM = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
    print("Connected to", self.DWM.name)
    
    self.ax, self.ay = [0, 0]
    self.bx, self.by = [300, 214]
    self.cx, self.cy = [0, 428]
    self.alldistance = [None for n in range(3)]
    
    # Start calculate distance
    time.sleep(0.5)
    print("Start calculate distance")
    distanceCMD = "AT+switchdis=1\r\n"
    self.DWM.write(distanceCMD.encode())
    time.sleep(1)
    
  def end(self):
    cmd = "AT+switchdis=0\r\n"
    self.DWM.write(cmd.encode())
    self.DWM.close()

  def distance(self):
  	while True:
  		data = self.DWM.readline().decode()
  		if "an0" in data:
  			print("Anchor0:", data[4:].strip())
  			self.alldistance[0] = float(data[4:-3])*100
  		if "an1" in data:
  			print("Anchor1:", data[4:].strip())
  			self.alldistance[1] = float(data[4:-3])*100
  		if "an2" in data:
  			print("Anchor2:", data[4:].strip())
  			self.alldistance[2] = float(data[4:-3])*100
        
  def triposition(self):
    x, y = sympy.symbols('x y')
    f1 = 2*x*(self.ax-self.cx)+np.square(self.cx)-np.square(self.ax)+2*y*(self.ay-self.cy)+np.square(self.cy)-np.square(self.ay)-(np.square(self.alldistance[2])-np.square(self.alldistance[0]))
    f2 = 2*x*(self.bx-self.cx)+np.square(self.cx)-np.square(self.bx)+2*y*(self.by-self.cy)+np.square(self.cy)-np.square(self.by)-(np.square(self.alldistance[2])-np.square(self.alldistance[1]))
    result = sympy.solve([f1, f2], [x, y])
    locx, locy = result[x], result[y]
  
    return locx, locy
