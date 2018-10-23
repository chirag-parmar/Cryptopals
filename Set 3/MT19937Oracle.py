from MT19937 import MT19937
import random
import time

globalMT = MT19937(5987)

def generateOracle():
	
	waitTime_1 = random.randint(40, 1000)
	waitTime_2 = random.randint(40, 1000)
	
	time.sleep(waitTime_1)
	
	mt = MT19937(int(time.time()))
	
	time.sleep(waitTime_2)
	
	first = mt.temper()
	
	return first

def temperOracle():
	global globalMT
	return globalMT.temper()


if __name__ == "__main__":
	print generateOracle()
	print temperOracle()