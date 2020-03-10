import os
import time
import numpy as np

def init_pwm():
	os.system("sudo ./pwm.sh")	

def set_pwm(u1, pin) :
	os.system("sudo echo " + str(u1*500000 + 1500000) + " > /sys/class/pwm/pwmchip0/pwm" + str(pin) + "/duty_cycle")

while 1:
	init_pwm()
	#for command in np.arange(-1.0, 1.0, 0.05):
	#	time.sleep(0.4)
	#	print(command)
	#	set_pwm(command, 0)