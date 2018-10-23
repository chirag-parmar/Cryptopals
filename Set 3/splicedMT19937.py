from MT19937Oracle import temperOracle
from MT19937 import MT19937

def untemper(y):

	c = 0xEFC60000
	t = 15 
	l = 18
	
	y ^= (y>>l)
	y ^= ((y<<t) & c)
	y = undoStepTwo(y)
	y = undoStepOne(y)

	return y

def undoStepTwo(y):
	
	b = 0x9D2C5680
	s = 7
	
	temp = y
	for i in range(5):
		temp <<= s
		temp = y ^ (temp & b)
	
	return temp

def undoStepOne(y):
	
	u = 11
	
	temp = y
	for i in range(2):
		temp >>= u
		temp ^= y

	return temp

mt = MT19937(12345)
state = []

for i in range(624):
	state.append(untemper(temperOracle()))

mt.setState(state)
mt.regenerate()
print mt.temper()
print temperOracle()


'''
4th Step Reversal

11010011
00001101 - 4 bit right shift and XOR
--------
11011110
--------
first 'l' bits of information is retained

since l> 1/2 of word size we can reverse this
1100 original - keep aside
XOR the remaining bits with the l original bits

BETTER method right shift 'l' bits again and XOR

11011110
00001101
--------
11010011 - original
--------

3rd Step Reversal

11010011
10011000 - 3 bit left shift
11100000 - mask
--------
10000000
11010011 - XOR with original
--------
01010011 - second half bits retained + last bit of first half retained

keep the second half bits + last bit of the first half aside

better method
left shift 't' bits, remask and then XOR with given bits

10011000 - left shift 3 bits
11100000 - mask
--------
10000000
01010011 - XOR with answer bits
--------
11010011

2nd Step Reversal

1010010101101010
1010110101000000 - 5 bits left shift
1010101010100000 - mask the last 5 bits
----------------
1010100000000000
1010010101101010 - XOR with original
----------------
0000110101101010 - last 5 bits retained


1010110101000000 - left shift 5 bits
1010101010100000 - mask the last 5 bits
----------------
1010100000000000 
0000110101101010 - XOR with given one
----------------
1010010101101010 - you have the last 10 bits right

repeat the same until the output of the routine is equal to the given one - repeat 5 times
1010110101000000 - 5 bits left shift
1010101010100000 - mask the last 5 bits
----------------
1010100000000000
1010010101101010 - XOR with previous answer
----------------
0000110101101010 - same Output

1st step Reversal

1010010101101010
0000001010010101 - right shift and XOR
----------------
1010011111111111
----------------

right shift and XOR until you get the same output - repeat 2 times

'''