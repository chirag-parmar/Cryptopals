from MT19937 import initialize, regenerate, temper
import random
import time

def generateOracle():
	
	waitTime_1 = random.randint(40,1000)
	waitTime_2 = random.randint(40,1000)
	
	time.sleep(waitTime_1)
	
	state = initialize(int(time.time()))
	
	time.sleep(waitTime_2)
	
	first = temper(state)
	
	return first

if __name__ == "__main__":
	print generateOracle()