import RPi.GPIO as gen
import time
import board
import busio
import adafruit_adxl34x
import math
import json

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

gen.setmode(gen.BCM)

SENSOR_PIN = 14

Sensor = []

gen.setup(SENSOR_PIN, gen.IN)

try:
	while True:
		obstacle_state = gen.input(SENSOR_PIN)
		xVal, yVal, zVal = accelerometer.acceleration
		
		if obstacle_state == gen.LOW:
			
			thetaX = math.atan(xVal / math.sqrt((yVal * yVal) + (zVal *zVal))) * 180 / math.pi
			thetaY = math.atan(yVal / math.sqrt((xVal * xVal) + (zVal *zVal))) * 180 / math.pi
			thetaZ = math.atan(math.sqrt((yVal * yVal) + (xVal *xVal)) / zVal) * 180 / math.pi
			
			timeStamps = [thetaX, thetaY, thetaZ]
			
			seconds = time.time()
			currentTime = time.ctime(seconds)
			
			axisDict = {
				currentTime: timeStamps}
			
			print(f"Hora a la que se obtuvo: {currentTime} - X : {thetaX} Y : {thetaY} Z : {thetaZ}")
			time.sleep(3)	
			
			Sensor.append(axisDict)
		
			json_object = json.dumps(Sensor, indent=4)
    
			with open("sample.json", "w") as outfile:
				outfile.write(json_object)
		
		else:				
			print('No hay nada')
		
except KeyboardInterrupt:
	gen.cleanup()