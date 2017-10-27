import redblacktree

class RangeTree(redblacktree.BinarySearchTree):
	def __init__(self, root=None, *initial_keys, **kwargs):
		super().__init__(root, *initial_keys)

		self.dimensions = kwargs['dimensions']

		if self.dimensions > 2:
			raise NotImplementedError("Max dimensions is 2")
		elif self.dimensions == 2:
			self._create_extra_trees()

	def _create_extra_trees(self):
		pass

	def LCS(self, node1, node2):
		if node1.key >= node2.key:
			node1, node2 = node2, node1

		node = self.root

		while node:
			if node1.key <= node.key <= node2.key:
				return node

			elif node.key < node2.key:
				node = node.right

			else:
				node = node.left

		# base case, shouldn't occur unless given nodes
		# not in tree
		return None

def test():
	array = [1,3,5,10,29,38,4,21,15,16,23,25]
	tree = RangeTree(*array)
	a = tree.find(1)
	b = tree.find(25)
	print(tree.LCS(a,b))

if __name__ == '__main__':
	test()

