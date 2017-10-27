from mpmath import mp

"Implementation of Fast Fourier Transform Algorithm"

PI = mp.pi
i = mp.j

A = (5,3,2,1)
B = (3,4,0,2)

def FFT(a):
	n = len(a)
	assert n & n - 1 == 0 # n is a power of 2
	
	if n == 1:
		return a

	
	root_unity_base = mp.exp(2*PI*i/n)
	root_unity = 1
	root_unity_base = mp.chop(root_unity_base)

	a_even = [elem for x, elem in enumerate(a) if x % 2 == 0]
	a_odd = [elem for x, elem in enumerate(a) if x % 2 == 1]

	y_even = FFT(a_even)
	y_odd = FFT(a_odd)

	y = [0] * n
	for k in range(n//2):
		# A(x) = A_even(x^2) + x * A_odd(x^2)
		# y[k] = A(omega k n)
		# y_even[k] = a_even(omega k n)^2 = a_even(omega k n/2)
		# 										^ already calculated
		t = mp.chop(root_unity*y_odd[k])
		y[k] = y_even[k] + t
		# opposite side of unit circle has same value y_even and y_odd:
		# i.e. (omega k n)^2 == (omega k+n/2 n)^2 == (omega k n/2)
		# however, actual omega is negative
		y[k + (n//2)] = y_even[k] - t
		root_unity *= root_unity_base
	return y

def inverse_FFT(points):
	n = len(points)
	points = [mp.conj(x) for x in points]
	a = FFT(points)
	a = [round(x/n) for x in a]
	return a

def polynomial_multiply(a,b):
	assert len(a) == len(b)
	size = len(a)
	boost = tuple(0 for x in range(size))
	a += boost
	b += boost
	points_a = FFT(a)
	points_b = FFT(b)
	points_c = [x*y for x,y in zip(points_a, points_b)]
	c = inverse_FFT(points_c)
	return c

result = polynomial_multiply(A,B)
print(result)