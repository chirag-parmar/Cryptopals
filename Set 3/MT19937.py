import ctypes

#MT19937 constants
w, n, m, r = (32, 624, 397, 31)
a = 0x9908B0DF
d = 0xFFFFFFFF
b = 0x9D2C5680
c = 0xEFC60000
f = 0x6c078965
u = 11
s = 7
t = 15 
l = 18

iterator = 0

def initialize(seed):
	if not type(seed) == type(1):
		raise Exception("Seed must be of type Integer")
	state = [seed]

	for i in range(1, n):
		prev = state[-1]
		curr = f * (prev^(prev >> (w-2))) + i
		state.append(ctypes.c_uint32(curr).value)

	state = regenerate(state)

	return state

def regenerate(state):
	global iterator

	for i in xrange(624):
		
		y = state[i] & 0x80000000
		y += state[(i + 1) % n] & 0x7fffffff
		
		z = state[(i + m) % n]
		
		state[i] = z^(y>>1)
		
		if y % 2:
			state[i] ^= a

	iterator = 0

	return state

def temper(state):
	global iterator

	if iterator>=n:
		if iterator>n:
			raise Exception("Unintialized State Array")
		regenerate(state)
	
	y = state[iterator]

	y ^= ctypes.c_uint32(y>>u).value
	y ^= ctypes.c_uint32((y<<s) & b).value
	y ^= ctypes.c_uint32((y<<t) & c).value
	y ^= ctypes.c_uint32(y>>l).value

	iterator += 1

	return y

if __name__ == "__main__":
	state = initialize(0000)
	randomSequence = ''
	for i in range(0,500):
		randomSequence += str(temper(state))

	print randomSequence