class BinarySearchTree():
	def __init__(self,root=None,*initial_keys):
		self.root = None if root == None else Node(root)

		if not initial_keys:
			return

		for key in initial_keys:
			self.insert(key)

	def insert(self,key):
		new_node = Node(key)

		if not self.root:
			self.root = new_node
			self.root.parent = nil_node
			return

		curr_node = self.root
		while True:
			if key < curr_node.key:
				if not curr_node.left:
					curr_node.left = new_node
					break
				else:
					curr_node = curr_node.left
			elif key > curr_node.key:
				if not curr_node.right:
					curr_node.right = new_node
					break
				else:
					curr_node = curr_node.right
			else:
				raise NotImplementedError("No duplicates allowed yet")

		new_node.parent = curr_node
		new_node.color = 'red'

		self._RB_restore_insert(new_node)

	def _RB_restore_insert(self,node):
		while node.parent.color == 'red':
			if node.parent.is_left_child():
				uncle = node.parent.parent.right
				# Case 1: uncle is red
				if uncle.color == 'red':
					node.parent.color = 'black'
					uncle.color = 'black'
					node.parent.parent.color = 'red'
					node = node.parent.parent
				# Cases 2 and 3: uncle is black
				else:
					# Case 2: if node is right child, turn to left child
					if node.is_right_child():
						node = node.parent
						self.left_rotate(node)
					# Case 3: if node is left child
					node.parent.color = 'black'
					node.parent.parent.color = 'red'
					self.right_rotate(node.parent.parent)
			# if node.parent is a right child
			else:
				uncle = node.parent.parent.left
				if uncle.color == 'red':
					node.parent.color = 'black'
					uncle.color = 'black'
					node.parent.parent.color = 'red'
					node = node.parent.parent

				else:
					if node.is_left_child():
						node = node.parent
						self.right_rotate(node)

					node.parent.color = 'black'
					node.parent.parent.color = 'red'
					self.left_rotate(node.parent.parent)

		self.root.color = 'black'

	def left_rotate(self,node):
		if not node.right:
			raise ValueError("Cannot left rotate node: %s" % (node))

		temp = nil_node

		self._transplant(node,node.right)
		node.parent = node.right
		if node.right.left:
			temp = node.right.left
			node.right.left.parent = node
		node.right.left = node
		node.right = temp

	def right_rotate(self,node):
		if not node.left:
			raise ValueError("Cannot right rotate node: %s" % (node))

		temp = nil_node

		self._transplant(node,node.left)
		node.parent = node.left
		if node.left.right:
			temp = node.left.right
			node.left.right.parent = node
		node.left.right = node
		node.left = temp

	def delete (self,node):
		# Handle 0 or 1 child case
		replacement = node
		replacement_orig_color = replacement.color
		if not node.left:
			# x = replacement of replacement
			x = node.right
			self._transplant(node,node.right)
		elif not node.right:
			x = node.left
			self._transplant(node,node.left)
		# Handle 2 child case
		else:
			replacement = self.min(node.right)
			replacement_orig_color = replacement.color
			x = replacement.right
			if not x:
				x.parent = replacement
			# Case if replacement is not right child of node
			if replacement.parent != node:
				self._transplant(replacement,replacement.right)
				replacement_is_right_child = False
			else:
				replacement_is_right_child = True
			self._transplant(node,replacement)
			if not replacement_is_right_child:
				node.right.parent = replacement
				replacement.right = node.right
			replacement.color = node.color
			replacement.left = node.left
			replacement.left.parent = replacement

		if replacement_orig_color == 'black':
			self._RB_restore_delete(x)

	def _transplant(self,node,replacement):
		if not node.parent:
			self.root = replacement
		elif node.is_left_child():
			node.parent.left = replacement
		else:
			node.parent.right = replacement
		replacement.parent = node.parent

	def _RB_restore_delete(self,node):
		# Loop maintains node is not root and node is doubly-black
		while node != self.root and node.color == 'black':
			if node.is_left_child():
				sibling = node.parent.right
				# Case 1: sibling - red
				if sibling.color == 'red':
					sibling.color = 'black'
					node.parent.color = 'red'
					self.left_rotate(node.parent)
					sibling = node.parent.right
				# Case 2: sibling, sibling right, sibling left - all black
				if sibling.left.color == 'black' and sibling.right.color == 'black':
					sibling.color = 'red'
					node = node.parent
				else:
					# Case 3: sibling - black, sibling right - black, sibling left - red
					if sibling.right.color == 'black':
						sibling.left.color = 'black'
						sibling.color = 'red'
						self.right_rotate(sibling)
						sibling = node.parent.right
					# Case 4: sibling - black, sibling right - red
					sibling.color = node.parent.color
					node.parent.color = 'black'
					sibling.right.color = 'black'
					self.left_rotate(node.parent)
					node = self.root # exit loop
			# if node is a right child
			else:
				sibling = node.parent.left
				if sibling.color == 'red':
					sibling.color = 'black'
					node.parent.color = 'red'
					self.right_rotate(node.parent)
					sibling = node.parent.left

				if sibling.left.color == 'black' and sibling.right.color == 'black':
					sibling.color = 'red'
					node = node.parent

				else:
					if sibling.left.color == 'black':
						sibling.right.color = 'black'
						sibling.color = 'red'
						self.left_rotate(sibling)
						sibling = node.parent.left
					sibling.color = node.parent.color
					node.parent.color = 'black'
					sibling.left.color = 'black'
					self.right_rotate(node.parent)
					node = self.root

		node.color = 'black'

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
		yield from self.inorder_traversal(self.root,'node')

	def __len__(self):
		return len(self.nodes)

class Node():
	__slots__ = ('key','right','left','parent','height','color')

	def __init__(self,key):
		self.key = key
		self.right = nil_node
		self.left = nil_node
		self.parent = nil_node

		self.color = 'black'

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
		return "Node: " + str(self.key) + " " + self.color

class NilNode(Node):
	def __init__(self):
		self.parent = None
		self.color = 'black'

	def __bool__(self):
		return False

	def __repr__(self):
		return "NilNode"

nil_node = NilNode()

def test():
	array = [1,3,5,10,29,38,4,21,15,16,23,25]
	tree = BinarySearchTree(*array)
	tree.delete(tree.find(29))
	print(tree.root.left.right.left)
	print('-----------------------------------')
	for key in tree:
		print('ITER --',key)

if __name__ == '__main__':
	test()