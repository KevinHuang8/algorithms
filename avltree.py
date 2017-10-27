class AVLTree():
	def __init__(self,root=None,*initial_keys):
		self.nodes = []

		self.root = None if root == None else Node(root)

		if not initial_keys:
			return

		for key in initial_keys:
			self.insert(key)

	def insert(self,key):
		new_node = Node(key)

		if not self.root:
			self.root = new_node
			return

		curr_node = self.root
		while True:
			if key < curr_node.key:
				if not curr_node.left:
					curr_node.left = new_node
					new_node.parent = curr_node
					break
				else:
					curr_node = curr_node.left
			elif key > curr_node.key:
				if not curr_node.right:
					curr_node.right = new_node
					new_node.parent = curr_node
					break
				else:
					curr_node = curr_node.right
			else:
				raise NotImplementedError("No duplicates allowed yet")

		self.rebalance(new_node)
		self.nodes.append(new_node)

	def delete (self,node):
		self.nodes.remove(node)

		if not node.left:
			self._transplant(node,node.right)
		elif not node.right:
			self._transplant(node,node.left)
		else:
			replacement = self.min(node.right)
			if replacement.parent != node:
				self._transplant(replacement,replacement.right)
				replacement_is_right_child = False
			else:
				replacement_is_right_child = True
			self._transplant(node,replacement)
			if not replacement_is_right_child:
				node.right.parent = replacement
				temp = replacement.right
				replacement.right = node.right
			else:
				temp = replacement
			replacement.left = node.left
			replacement.left.parent = replacement

			self.rebalance(temp)

	def _transplant(self,node,replacement):
		if not node.parent:
			self.root = replacement
		elif node.is_left_child():
			node.parent.left = replacement
		else:
			node.parent.right = replacement
		if replacement:
			replacement.parent = node.parent

	def find(self,key):
		curr_node = self.root
		while curr_node:
			if key == curr_node.key:
				return curr_node
			elif key < curr_node.key:
				curr_node = curr_node.left
			elif key > curr_node.key:
				curr_node = curr_node.right
		return None

	def min(self,curr_node):
		while curr_node.left:
			curr_node = curr_node.left
		return curr_node

	def max(self,curr_node):
		while curr_node.right:
			curr_node = curr_node.right
		return curr_node

	def successor(self,node):
		if node.right:
			return self.min(node.right)

		while node.parent:
			if node.is_right_child():
				node = node.parent
			else:
				return node.parent

	def predecessor(self,node):
		raise NotImplementedError("doesn't work yet")

		if node.left:
			return self.max(node.left)

		if node.parent:
			if node.is_right_child():
				return node.parent
		return None

	def left_rotate(self,node):
		if not node.right:
			raise ValueError("Cannot left rotate node: %s" % (node))

		temp = None

		self._transplant(node,node.right)
		node.parent = node.right
		if node.right.left:
			temp = node.right.left
			node.right.left.parent = node
		node.right.left = node
		node.right = temp
		self.update_height(node)
		self.update_height(node.parent)

	def right_rotate(self,node):
		if not node.left:
			raise ValueError("Cannot right rotate node: %s" % (node))

		temp = None

		self._transplant(node,node.left)
		node.parent = node.left
		if node.left.right:
			temp = node.left.right
			node.left.right.parent = node
		node.left.right = node
		node.left = temp
		self.update_height(node)
		self.update_height(node.parent)

	def height(self,node):
		if not node:
			return -1
		else:
			return node.height

	def update_height(self,node):
		node.height = max(self.height(node.left), self.height(node.right)) + 1

	def _is_right_heavy(self,node,max_balance_factor=1):
		if self.height(node.right) - self.height(node.left) > max_balance_factor:
			return True
		else:
			return False

	def _is_left_heavy(self,node,max_balance_factor=1):
		if self.height(node.left) - self.height(node.right) > max_balance_factor:
			return True
		else:
			return False

	def rebalance(self,node):
		while node:
			self.update_height(node)
			if self._is_right_heavy(node):
				if self._is_left_heavy(node.right,0):
					self.right_rotate(node.right)
				self.left_rotate(node)

			elif self._is_left_heavy(node):
				if self._is_right_heavy(node.left,0):
					self.left_rotate(node.left)
				self.right_rotate(node)

			node = node.parent

	def inorder_traversal(self,curr_node,display='key'):
		if curr_node:

			yield from self.inorder_traversal(curr_node.left,display)

			if display == 'key':
				yield curr_node.key
			elif display == 'node':
				yield curr_node
			else:
				raise Exception('Invalid display type: %s' % (display))

			yield from self.inorder_traversal(curr_node.right,display)

	def __iter__(self):
		yield from self.inorder_traversal(self.root)

	def __len__(self):
		return len(self.nodes)

class Node():
	__slots__ = ('key','right','left','parent','height')

	def __init__(self,key):
		self.key = key
		self.right = None
		self.left = None
		self.parent = None
		self.height = 0

	def is_left_child(self):
		if not self.parent:
			return False

		if self == self.parent.left:
			return True
		else:
			return False

	def is_right_child(self):
		if not self.parent:
			return False

		if self == self.parent.right:
			return True
		else:
			return False

	def __repr__(self):
		return "Node object: " + str(self.key) + " h: " + str(self.height)

tree = AVLTree(1,3,5,10,29,38,4,21,15,16,23,25)
for key in tree:
	print(key)