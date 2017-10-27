from profilehooks import profile

class DisjointSetList:
	def __init__(self):
		self.sets = set()
		self.key_to_object = {}

	def new_set(self, key):
		assert key not in self.key_to_object, "Keys must be distinct"

		new_set = SingleSet()
		new_node = LinkedNode(key)
		new_node.membership = new_set
		new_set.head = new_node
		new_set.tail = new_node

		self.sets.add(new_set)
		self.key_to_object[key] = new_node

	def find(self, key):
		if key not in self.key_to_object:
			raise KeyError("Key not found in any set: %s" % (key))
		node = self.key_to_object[key]
		return node.membership

	def union(self, set1, set2):
		assert isinstance(set1, SingleSet) and isinstance(set2, SingleSet)
		assert set1 in self.sets and set2 in self.sets, "Set not found"

		if set1.weight >= set2.weight:
			heavier = set1
			lighter = set2
		else:
			heavier = set2
			lighter = set1

		for node in lighter:
			node.membership = heavier

		heavier.tail.next = lighter.head
		heavier.tail = lighter.tail

		heavier.weight += lighter.weight

		self.sets.remove(lighter)

	def __iter__(self):
		for set_ in self.sets:
			yield set_

class LinkedNode:
	def __init__(self, key):
		self.key = key
		self.membership = None
		self.next = None

	def __repr__(self):
		return "<LinkedNode(key: %s)>" % (self.key)

class SingleSet:
	def __init__(self):
		self.weight = 1
		self.head = None
		self.tail = None

	def __iter__(self):
		node = self.head

		while node != None:
			yield node
			node = node.next

	def __repr__(self):
		return str(tuple(elem.key for elem in self))

class DisjointSet:
	def __init__(self):
		self.sets = set()
		self.key_to_object = {}

	def new_set(self, key):
		assert key not in self.key_to_object, "Keys must be distinct"
		new_node = TreeNode(key)
		self.key_to_object[key] = new_node
		self.sets.add(new_node)

	def find(self, key):
		if key not in self.key_to_object:
			raise KeyError("Key not found in any set: %s" % (key))
		node = self.key_to_object[key]

		def _find(node):
			if node != node.parent:
				node.parent = _find(node.parent)
			return node.parent

		return _find(node)

	def union(self, root1, root2):
		if root1.rank > root2.rank:
			root2.parent = root1
			self.sets.remove(root2)
		else:
			root1.parent = root2
			self.sets.remove(root1)
			if root1.rank == root2.rank:
				root2.rank += 1

class TreeNode:
	def __init__(self, key):
		self.key = key
		self.parent = self
		self.rank = 0

	def __repr__(self):
		return "<TreeNode(key: %s)>" % (self.key)