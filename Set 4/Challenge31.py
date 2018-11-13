import numpy as np
import matplotlib.pyplot as plt
import threading
import requests
import random
import time
import os

num_of_samples = 1
max_num_parallel_samples = 1
max_num_parallel_guess = 1

def findRoundTiming(url, signature, timings):
	
	try:
		start = float(time.time())
		response = requests.get(url = url + signature)
		if response.status_code == 500:
			td = response.elapsed
			timings.append((td.microseconds + (td.seconds + td.days * 24.00 * 3600.00) * 10.00**6) / 10.00**3)
		elif response.status_code == 200:
			print "Awesome Luck, Found Signature: " + signature
	except:
		timings.append(np.nan)

	return True

def makeGuess(guess, url, signature, byte_num, char_timings):
	signature = signature[:byte_num*2] + hex(guess)[2:].zfill(2) + signature[((byte_num*2)+2):]
	timings = []

	for j in range(0, num_of_samples, max_num_parallel_samples):
		processes = []
		for i in range(j, j + max_num_parallel_samples):
			time.sleep(0.002)
			process = threading.Thread(target=findRoundTiming, args=(url, signature, timings))
			process.start()
			processes.append(process)

		for process in processes:
			process.join()

	char_timings.append(timings)

	if guess%32 == 0:
		print str(guess/32 + 1) + "...",
	
	return True

def findByte(url, signature, byte_num):
	
	char_timings = []

	startTiming = time.time()	
	
	for j in range(0, 256, max_num_parallel_guess):
		threads = []
		for i in range(j, j + max_num_parallel_guess):
			time.sleep(0.002)
			thread = threading.Thread(target=makeGuess, args=(i, url, signature, byte_num, char_timings))
			thread.start()
			threads.append(thread)

		for thread in threads:
			thread.join()
		
	
	print
	print time.time() - startTiming

	timingData = np.matrix(char_timings)

	timingData = np.nanmean(timingData, axis=1)

	plt.plot(timingData)
	plt.show()

	foundChar = np.argmax(timingData)

	return signature[:byte_num*2] + hex(foundChar)[2:].zfill(2).rstrip('L') + signature[((byte_num*2)+2):]

def timingAttack(message):

	BASE_URL = "http://localhost:8080/test?file=" + message.replace(" ", "%20") + "&signature="
	signature = "00"*20

	for i in range(0,20):
		signature = findByte(BASE_URL, signature, i)
		print signature

if __name__ == "__main__":
	timingAttack("Chirag is a good guy")