import random
import math
from collections import defaultdict
from profilehooks import profile

class SkipList:
	
	max_height = 32

	def __init__(self):
		self.start = SkipNode(-math.inf, None, math.inf)
		self.end = SkipNode(math.inf, None, math.inf)
		for h in range(SkipList.max_height + 1):
			self.start.next[h] = self.end
		self._top_level = -1
		self._length = 0
		self._elements = defaultdict(int)

	def _insert(self, key, val):
		assert isinstance(key, int), "Only supports integer keys"
		self._length += 1
		self._elements[key] += 1

		height = 0
		while random.randint(0,1) == 1:
			height += 1

		new_node = SkipNode(key, val, height)

		if new_node.height > self._top_level:
			self._top_level = new_node.height

		prev_node = self.search(key, True)
		height = min(prev_node.height, new_node.height)
		
		while height >= 0:			
			new_node.next[height] = prev_node.next[height]
			prev_node.next[height] = new_node
			height -= 1

		if new_node.height > prev_node.height:
			for h in range(prev_node.height + 1, new_node.height + 1):
				curr_node = self.start
				while curr_node != self.end:
					next_node = curr_node.next[h]
					if next_node.key > new_node.key:
						curr_node.next[h] = new_node
						new_node.next[h] = next_node
						break
					curr_node = next_node

	def delete(self, key):
		to_delete = self.search(key)

		if to_delete == None:
			raise KeyError("Key '%s' not found" % (key))

		self._length -= 1
		self._elements[key] -= 1
		if self._elements[key] == 0:
			del self._elements[key]

		prev_node = self.search(key - 1, True)

		height = min(prev_node.height, to_delete.height)

		while height >= 0:
			prev_node.next[height] = to_delete.next[height]
			height -= 1

		if to_delete.height > prev_node.height:
			for h in range(prev_node.height + 1, to_delete.height + 1):
				curr_node = self.start
				while curr_node != self.end:
					next_node = curr_node.next[h]
					if next_node == to_delete:
						curr_node.next[h] = next_node.next[h]
						break
					curr_node = next_node

	def search(self, key, less_than=False):
		level = self._top_level
		curr_node = self.start

		while level >= 0:
			next_node = curr_node.next[level]
			if next_node.key == key:
				return next_node
			elif next_node.key > key:
				level -= 1
			else:
				curr_node = next_node

		# If less_than flag activated, if node not found,
		# return greatest node less than key
		if less_than:
			return curr_node

		return None

	def __setitem__(self, key, val):
		self._insert(key, val)

	def __getitem__(self, key):
		return self.search(key).val

	def __contains__(self, key):
		return key in self._elements

	def __repr__(self):
		return str(self._elements)

	def __iter__(self):
		yield from self.traverse('key')

	def items(self):
		yield from self.traverse('items')

	def nodes(self):
		yield from self.traverse('node')

	def values(self):
		yield from self.traverse('val')

	def traverse(self, attr):
		curr_node = self.start
		next_node = curr_node.next[0]
		while next_node != self.end:
			if attr == 'key':
				yield next_node.key
			elif attr == 'val':
				yield next_node.val
			elif attr == 'items':
				yield (next_node.key, next_node.val)
			elif attr == 'node':
				yield next_node
			else:
				raise Exception("Invalid traversal type: %s" % (attr))
			curr_node = next_node
			next_node = curr_node.next[0]

	def __bool__(self):
		return bool(self._elements)

	def __len__(self):
		return self._length

class SkipNode:

	def __init__(self, key, val, height, start=False):
		self.key = key
		self.val = val
		self.height = height
		self.next = {}

	def __repr__(self):
		return "<Key: " + str(self.key) + " Value: " + str(self.val) + " Height: " + str(self.height) + ">"

	def __str__(self):
		return "<k: %s, v: %s>" % (self.key, self.val)

if __name__ == '__main__':
	a = SkipList()
	for i in range(250):
		a[i] = 15
	for i in range(250):
		a.search(i)
	for i in range(250):
		a.delete(i)

