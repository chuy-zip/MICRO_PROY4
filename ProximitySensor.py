# The code is importing various Python modules that are needed for the program to run:
import RPi.GPIO as gen
import time
import board
import busio
import adafruit_adxl34x
import math
import json

# The line `i2c = busio.I2C(board.SCL, board.SDA)` is initializing the I2C (Inter-Integrated Circuit)
# communication bus using the pins `board.SCL` and `board.SDA`. These pins are specific to the
# Raspberry Pi board and are used for I2C communication with external devices. The `busio.I2C` class
# is provided by the `busio` module in the Adafruit CircuitPython library, and it allows communication
# with I2C devices connected to the Raspberry Pi.
i2c = busio.I2C(board.SCL, board.SDA)

# The line `accelerometer = adafruit_adxl34x.ADXL345(i2c)` is creating an instance of the `ADXL345`
# class from the `adafruit_adxl34x` module. This class represents an accelerometer sensor,
# specifically the ADXL345 model. The `ADXL345` class requires an `i2c` object as a parameter, which
# is the I2C communication bus that is initialized earlier in the code. By creating an instance of the
# `ADXL345` class, we can interact with the accelerometer sensor and retrieve acceleration data from
# it.
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# `gen.setmode(gen.BCM)` is setting the numbering mode for the GPIO pins on the Raspberry Pi to BCM
# (Broadcom SOC channel).
gen.setmode(gen.BCM)

SENSOR_PIN = 14 # Using GPIO pin number 14

Sensor = [] # Using a list to store the dictionaries

# The line `gen.setup(SENSOR_PIN, gen.IN)` is setting up the GPIO pin specified by `SENSOR_PIN` as an
# input pin. This means that the pin will be used to read the state of an external sensor or device.
# In this case, it is likely that the pin is connected to a proximity sensor or obstacle detection
# sensor. By setting the pin as an input, the code can later use `gen.input(SENSOR_PIN)` to read the
# state of the sensor (whether an obstacle is detected or not).
gen.setup(SENSOR_PIN, gen.IN)

# The code inside the `try` block will be executed if the sensor is detected, otherwise, it will throw
# an exception and clean the GPIO registers.
try:

	# The code block `while True:` is a loop that continuously runs until it is interrupted. Within the
	# loop, the code reads the state of an obstacle detection sensor using `obstacle_state =
	# gen.input(SENSOR_PIN)`. It then retrieves acceleration data from an accelerometer using `xVal,
	# yVal, zVal = accelerometer.acceleration`.
	while True:
		obstacle_state = gen.input(SENSOR_PIN)
		xVal, yVal, zVal = accelerometer.acceleration
		
		if obstacle_state == gen.LOW:
			
			# The code is calculating the angles of rotation around the X, Y, and Z axes based on the
			# acceleration values obtained from the accelerometer sensor.
			thetaX = math.atan(xVal / math.sqrt((yVal * yVal) + (zVal *zVal))) * 180 / math.pi
			thetaY = math.atan(yVal / math.sqrt((xVal * xVal) + (zVal *zVal))) * 180 / math.pi
			thetaZ = math.atan(math.sqrt((yVal * yVal) + (xVal *xVal)) / zVal) * 180 / math.pi
			
			# The line `timeStamps = [thetaX, thetaY, thetaZ]` is creating a list called `timeStamps` that
			# contains the values of `thetaX`, `thetaY`, and `thetaZ`. These values represent the angles of
			# rotation around the X, Y, and Z axes respectively, calculated based on the acceleration data
			# obtained from the accelerometer sensor. By storing these values in a list, they can be easily
			# accessed and used later in the code.
			timeStamps = [thetaX, thetaY, thetaZ]
			
			# The code `seconds = time.time()` is retrieving the current time in seconds since the epoch
			# (January 1, 1970). This value represents the number of seconds that have passed since that
			# specific point in time.
			seconds = time.time()
			currentTime = time.ctime(seconds)
			
			# The line `axisDict = {currentTime: timeStamps}` is creating a dictionary called `axisDict`. The
			# dictionary has a key-value pair, where the key is the current time (`currentTime`) and the value
			# is a list of the angles of rotation around the X, Y, and Z axes (`timeStamps`).
			axisDict = {
				currentTime: timeStamps}
			
			# The line `print(f"Hora a la que se obtuvo: {currentTime} - X : {thetaX} Y : {thetaY} Z :
			# {thetaZ}")` is printing a formatted string that displays the current time (`currentTime`) and the
			# values of the angles of rotation around the X, Y, and Z axes (`thetaX`, `thetaY`, `thetaZ`).
			print(f"Hora a la que se obtuvo: {currentTime} - X : {thetaX} Y : {thetaY} Z : {thetaZ}")

			# The line `time.sleep(3)` is causing the code to pause for 3 seconds before continuing to the next
			# iteration of the loop. This means that after the acceleration data is obtained and stored in the
			# `Sensor` list, the code will wait for 3 seconds before retrieving the next set of data. This
			# delay can be useful in scenarios where you want to control the rate at which data is collected or
			# to introduce a delay between consecutive measurements.
			time.sleep(3)	
			
			# `Sensor.append(axisDict)` is adding the dictionary `axisDict` to the `Sensor` list. This line of
			# code is used to store the acceleration data and corresponding timestamps in the `Sensor` list.
			# Each dictionary in the `Sensor` list represents a set of acceleration data and its corresponding
			# timestamp. By appending the `axisDict` dictionary to the `Sensor` list, the code is effectively
			# storing each set of acceleration data and timestamp in the list for later use or analysis.
			Sensor.append(axisDict)
		
			# The code `json_object = json.dumps(Sensor, indent=4)` is converting the `Sensor` list into a
			# JSON-formatted string. The `json.dumps()` function is a method provided by the `json` module in
			# Python, and it is used to convert a Python object (in this case, the `Sensor` list) into a JSON
			# string.
			json_object = json.dumps(Sensor, indent=4)
    
			with open("sample.json", "w") as outfile:
				outfile.write(json_object)
		
		else:				
			# The line `print('No hay nada')` is printing the string "No hay nada" to the console. This is a
			# message indicating that there is no obstacle detected by the sensor.
			print('No hay nada')
		
except KeyboardInterrupt:

	# `gen.cleanup()` is a function provided by the `RPi.GPIO` module in Python. It is used to clean up
	# the GPIO (General Purpose Input/Output) pins on the Raspberry Pi board.
	gen.cleanup()