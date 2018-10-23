import ctypes

class MT19937:

	def __init__(self, seed):
		self.w = 32
		self.n = 624
		self.m = 397
		self.a = 0x9908B0DF
		self.d = 0xFFFFFFFF
		self.b = 0x9D2C5680
		self.c = 0xEFC60000
		self.f = 0x6c078965
		self.u = 11
		self.s = 7
		self.t = 15 
		self.l = 18

		self.iterator = 0

		self.state = []

		if not type(seed) == type(1):
			raise Exception("Seed must be of type Integer")
		self.state = [seed]

		for i in range(1, self.n):
			prev = self.state[-1]
			curr = self.f * (prev^(prev >> (self.w-2))) + i
			self.state.append(ctypes.c_uint32(curr).value)

		self.regenerate()
	
	def reinitialize(self, seed):
		
		if not type(seed) == type(1):
			raise Exception("Seed must be of type Integer")

		self.state = []
		self.state = [seed]

		for i in range(1, self.n):
			prev = self.state[-1]
			curr = self.f * (prev^(prev >> (self.w-2))) + i
			self.state.append(ctypes.c_uint32(curr).value)

		self.regenerate()

	def regenerate(self):
		for i in range(self.w):
			
			y = self.state[i] & 0x80000000
			y += self.state[(i + 1) % self.n] & 0x7fffffff
			
			z = self.state[(i + self.m) % self.n]
			
			self.state[i] = z^(y>>1)
			
			if y % 2:
				self.state[i] ^= self.a

		self.iterator = 0

	def temper(self):

		if self.iterator>=self.n:
			if self.iterator>self.n:
				raise Exception("Unintialized state Array")
			self.regenerate()
		
		y = self.state[self.iterator]

		y ^= (y>>self.u)
		y ^= ((y<<self.s) & self.b)
		y ^= ((y<<self.t) & self.c)
		y ^= (y>>self.l)

		self.iterator += 1

		return ctypes.c_uint32(y).value

	def setState(self, state):
		self.state = state
		self.iterator = 0

if __name__ == "__main__":
	mt = MT19937(0000)
	randomSequence = ''
	for i in range(0,500):
		randomSequence += str(mt.temper())

	print randomSequence










