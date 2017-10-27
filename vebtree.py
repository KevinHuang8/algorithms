from math import sqrt, ceil

def most_significant_half(x, length):
	for _ in range(length//2):
		x >>= 1
	return x

def least_significant_half(x, length):
	i = 2**(length//2) - 1
	x &= i
	return x

class vEB():
	"Van Emde Boas Tree"
	def __init__(self, universe_size):
		self.u = 2
		while self.u < universe_size:
			self.u *= 2
		self.min = None
		self.max = None
		self.clusters = ()
		self.summary = None
		self.elements = {}

		if self.u > 2:
			self._create_subtrees()

	def _create_subtrees(self):
		subtree_size = ceil(sqrt(self.u))
		self.clusters = tuple(vEB(subtree_size) for _ in range(subtree_size + 1))
		self.summary = vEB(subtree_size)

	def insert(self, *keys):
		for key in keys:
			self.elements[key] = True
			self._insert(key)

	def _insert(self, key):
		if key >= self.u:
			raise ValueError("Key '%s' is too large. Max size is: %s" % (key, self.u))

		# Inserting into an empty tree
		if self.min == None:
			self._empty_insert(key)

		else:
			# Update min
			if key < self.min:
				key, self.min = self.min, key

			if self.u > 2:
				# If cluster that key will go into is empty
				if self.clusters[self._high(key)].min == None:
					# Summary has to be updated
					self.summary._insert(self._high(key))
					self.clusters[self._high(key)]._empty_insert(self._low(key))
				else:
					# Insert key as normal into the proper cluster
					self.clusters[self._high(key)]._insert(self._low(key))

			# Update max
			if key > self.max:
				self.max = key

	def _empty_insert(self, key):
		self.min = self.max = key

	def delete(self, *keys):
		for key in keys:
			self.elements
			self._delete(key)

	def _delete(self, key):
		if key >= self.u:
			raise ValueError("Key '%s' is too large. Max size is: %s" % (key, self.u))

		if key not in self:
			raise ValueError("Key not found: %s" % (key))

		self.elements[key] = False

		# If there is only one element
		if self.min == self.max:
			self.min = self.max = None

		elif self.u <= 2:
			# set min and max to the remaining element
			if key == 0:
				self.min = 1
			else:
				self.min = 0
			self.max = self.min

		else:
			if key == self.min:
				# the cluster that contains the next smallest element after 'key'
				first_cluster = self.summary.min
				# sets key to the next smallest element, and the min to that key
				key = self._index(first_cluster, self.clusters[first_cluster].min)
				self.min = key

			self.clusters[self._high(key)]._delete(self._low(key))
			# Tests whether the cluster deleted from has become empty
			if self.clusters[self._high(key)].min == None:
				self.summary._delete(self._high(key))
				# Update max when summary has been updated
				if key == self.max:
					summary_max = self.summary.max
					# If there are no elements except for min
					if summary_max == None:
						self.max = self.min
					else:
						self.max = self._index(summary_max, self.clusters[summary_max].max)

			# Update max when summary hasn't been updated
			elif key == self.max:
				self.max = self._index(self._high(key), self.clusters[self._high(key)].max)

	def successor(self, key):
		if key >= self.u:
			return None

		if self.u <= 2:
			# successor of 0 is 1 if 1 is present in base case
			if key == 0 and self.max == 1:
				return 1
			else:
				return None

		# successor of anything less than min is min
		elif self.min != None and key < self.min:
			return self.min

		else:
			# maximum element in cluster containing 'key'
			max_low = self.clusters[self._high(key)].max
			# successor must be within cluster if max > 'key'
			if max_low != None and self._low(key) < max_low:
				# Find successor within the cluster
				offset = self.clusters[self._high(key)].successor(self._low(key))
				return self._index(self._high(key), offset)

			else:
				# Search for the next cluster using summary
				succ_cluster = self.summary.successor(self._high(key))
				if succ_cluster == None:
					return None
				else:
					# Successor is the min in that cluster
					offset = self.clusters[succ_cluster].min
					return self._index(succ_cluster, offset)

	def predecessor(self, key):
		""" Symmetric to successor"""
		if key < 0:
			return None

		if self.u <= 2:
			if key == 1 and self.min == 0:
				return 0
			else:
				return None

		elif self.max != None and key > self.max:
			return self.max

		else:
			# min element in cluster containing 'key'
			min_low = self.clusters[self._high(key)].min
			# predecessor must be within cluster
			if min_low != None and self._low(key) > min_low:
				offset = self.clusters[self._high(key)].predecessor(self._low(key))
				return self._index(self._high(key), offset)

			else:
				# Otherwise, predecessor must be in preceding cluster, find using summary
				pred_cluster = self.summary.predecessor(self._high(key))
				if pred_cluster == None:
					# If the predecessor is the minimum, which doesn't reside in any cluster
					if self.min != None and key > self.min:
						return self.min
					else:
						return None
				else:
					offset = self.clusters[pred_cluster].max
					return self._index(pred_cluster, offset)

	def resize(self, universe_size):
		u = 2
		while u < universe_size:
			u *= 2

		if self.max > u:
			raise ValueError("Universe size '%s' is too big. Max element is '%s'" \
				% (self.max, universe_size))

		new_tree = vEB(u)
		for i in self:
			new_tree.insert(i)

		return new_tree

	def _high(self, key):
		"""Represents which cluster 'key' is in"""
		return int(key/int(sqrt(self.u)))
		return most_significant_half(key, int(sqrt(self.u)))

	def _low(self, key):
		"""Represents the position of 'key' within its cluster"""
		return key % int(sqrt(self.u))
		return least_significant_half(key, int(sqrt(self.u)))

	def _index(self, high, low):
		return high*int(sqrt(self.u)) + low

	def __contains__(self, key):
		# Membership test for subtrees
		if key >= self.u:
			return False
		if key == self.min or key == self.max:
			return True
		elif self.u <= 2:
			return False
		else:
			return self._low(key) in self.clusters[self._high(key)]

	def __iter__(self):
		"""O(n) but unordered. Also only gives discreet items."""
		for i in self.elements:
			yield i

	def ordered_items(self):
		"""O(n log log u) but ordered"""
		x = self.min
		while x != None:
			yield x
			x = self.successor(x)

	def __repr__(self):
		return "u: %s min: %s max: %s" \
		% (self.u, self.min, self.max)

def test():
	test_veb = vEB(128)
	t_insert = [2,3,4,5,7,14,15]
	test_veb.insert(*t_insert)
	test_veb = test_veb.resize(32)
	assert test_veb.min == 2
	assert test_veb.max == 15
	if test_veb.u == 16:
		assert test_veb.clusters[0].min == 3
		assert test_veb.clusters[2].min == None
		assert test_veb.summary.clusters[1].min == 1
	for i in t_insert:
		assert i in test_veb
	assert test_veb.summary.min == 0
	assert test_veb.successor(2) == 3
	assert test_veb.successor(7) == 14
	assert test_veb.successor(15) == None
	assert test_veb.successor(14) == 15
	assert test_veb.predecessor(16) == 15
	assert test_veb.predecessor(3) == 2
	assert test_veb.predecessor(14) == 7
	assert test_veb.predecessor(15) == 14
	assert test_veb.predecessor(20) == 15
	for i in test_veb:
		assert i in test_veb
	for i in test_veb.ordered_items():
		assert i in test_veb
	to_delete = [3,5,15]
	test_veb.delete(*to_delete)
	for i in to_delete:
		assert i not in test_veb
	assert test_veb.max == 14
	if test_veb.u == 16:
		assert test_veb.clusters[0].min == None
		assert test_veb.clusters[1].clusters[0].min == None
	assert test_veb.predecessor(4) == 2
	assert test_veb.predecessor(7) == 4
	assert test_veb.successor(14) == None
	
test()