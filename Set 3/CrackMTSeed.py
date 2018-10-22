from MT19937Oracle import generateOracle
from MT19937 import initialize, temper
import time

def crackTheSeed():
	startTime = int(time.time())
	randomOut = generateOracle()
	print randomOut
	endTime = int(time.time())

	for i in range(startTime, endTime+1):
		state = initialize(i)
		bruteOut = temper(state)
		if bruteOut == randomOut:
			print "Found the seed: " + str(i)


if __name__ == "__main__":
	crackTheSeed()