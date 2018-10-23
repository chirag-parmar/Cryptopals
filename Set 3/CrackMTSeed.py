from MT19937Oracle import generateOracle
from MT19937 import MT19937
import time

def crackTheSeed():
	startTime = int(time.time())
	randomOut = generateOracle()
	endTime = int(time.time())

	mt = MT19937(0)
	for i in range(startTime, endTime+1):
		mt.reinitialize(i)
		bruteOut = mt.temper()
		if bruteOut == randomOut:
			print "Found the seed: " + str(i)


if __name__ == "__main__":
	crackTheSeed()