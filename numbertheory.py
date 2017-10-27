from profilehooks import profile

def gcd(a, b):
	"""Euclid's algorithm for GCD"""
	if b == 0:
		return a
	else:
		return gcd(b, a % b)

def lcm(a, b):
	return a*b//gcd(a,b)

def extended_gcd(a, b):
	"""returns x, y such that d = ax + by"""
	if b == 0:
		return (a, 1, 0)
	else:
		_d, _x, _y = extended_gcd(b, a % b)
		d, x, y = _d, _y, _x - a//b*_y
		return d, x, y

def mod_lineareq_solver(a, b, n):
	"""Solves for all x in modular equation: ax = b (mod n)"""
	d, _x, _y = extended_gcd(a, n)
	x = set()
	if b % d == 0:
		x0 = (_x*(b//d)) % n
		x.add(x0)
		for i in range(d):
			x.add((x0 + i*(n//d)) % n)

	return x

def modular_exp(a, b, n):
	"""calculates a**b % n"""
	result = 1

	while b:
		# If digit is 1
		if b & 1:
			result = result * a % n

		b >>= 1
		a = a**2 % n

	return result

def witness(a, n):
	"""Return True if a is a witness to n being composite, False otherwise"""
	u = n - 1
	t = 0
	while u % 2 == 0:
		u //= 2
		t += 1

	x = {}
	x[0] = pow(a, u, n)
	for i in range(1, t + 1):
		x[i] = x[i - 1]**2 % n
		if x[i] == 1 and x[i - 1] != 1 and x[i - 1] != n - 1:
			return True
		del x[i - 1]

	if x[t] != 1:
		return True

	return False

import random
def miller_rabin(n, s=5):
	"""Return True if n is prime. s is number of tries"""
	for j in range(s):
		a = random.randint(2, n - 1)
		if witness(a, n):
			return False

	return True

def primality_test(n):
	if n < 2:
		return False

	low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 
	71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 
	167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 
	269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 
	379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 
	487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 
	607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 
	727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 
	853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 
	977, 983, 991, 997]

	if n in low_primes:
		return True

	for prime in low_primes:
		if n % prime == 0:
			return False

	return miller_rabin(n)

def generate_prime(size=512):
	for i in range(size*2):
		num = random.randrange(2**(size - 1), 2**(size))
		if primality_test(num):
			return num
	raise Exception("Failed to find prime in %s tries" % (size*2))

from math import sqrt
def sieve_of_eratosthenes(limit):
	primes = list(range(limit + 1))
	primes[1] = False

	for i in range(2, int(sqrt(limit)) + 1):
		if primes[i]:
			# set all multiples of i from i**2 onwards to 0
			primes[i**2 : limit + 1 : i] = [False] * len(range(i**2, limit + 1, i))

	return filter(None, primes)

def sum_primes(limit):
	total = 0
	for i in sieve_of_eratosthenes(limit):
		total += i
	return total

a = [129383,102938,93821,1000,7263491]
for x in a:
	for i in sieve_of_eratosthenes(10000):
		if x % i == 0:
			break
	else:
		print(x)


#print(gcd(304239402394283094280344234124089124124123123123124235234562980984302,
#	302344123401928239048712904781294234234231213056750238)) #=42
