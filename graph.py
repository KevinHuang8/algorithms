import math
from collections import defaultdict
from heap import heap
from disjointset import DisjointSet
from profilehooks import profile

class NegativeCycleException(Exception):
	def __init__(self, negative_cycle_verticies):
		super().__init__("Graph contains a negative cycle: %s" % (negative_cycle_verticies))
		self.negative_cycle_verticies = negative_cycle_verticies

class NoPathFound(Exception):
	pass

class Graph:
	def __init__(self, verticies=(), edges=(), is_directed=False):
		"""
		verticies - any iterable containing hashable objects
		edges - any iterable containing sets or tuples of length 2. Every element
		of the constituent sets/tuples must be in 'verticies'.
		"""
		self.is_directed = is_directed

		edges = self._convert_set_to_tuples(edges)

		self.verticies = set(verticies)
		self.edges = set(edges)

		self._setup_adjacency_map()

		self._reset_attributes()

		self.is_acyclic = self._is_acyclic()

	def breadth_first_search(self, starting_vertex):
		self.distance_from_start = defaultdict(lambda: None, {starting_vertex: 0})
		self.parents = defaultdict(lambda: None, {starting_vertex: None})
		level = 1
		frontier = [starting_vertex]
		while frontier:
			next_frontier = []
			for frontier_vertex in frontier:
				for adjacent_vertex in self.adjacency_map[frontier_vertex]:
					# if adjacent_vertex not yet seen
					if adjacent_vertex not in self.distance_from_start:
						self.distance_from_start[adjacent_vertex] = level
						self.parents[adjacent_vertex] = frontier_vertex
						next_frontier.append(adjacent_vertex)
			frontier = next_frontier
			level += 1

	def shortest_path(self, starting_vertex, ending_vertex):
		assert starting_vertex in self.verticies, \
		"Invalid starting vertex %s" % (starting_vertex)
		assert ending_vertex in self.verticies, \
		"Invalid ending vertex %s" % (ending_vertex)

		# if self.distance_from_start not yet computed, compute it
		if not self.distance_from_start or self.distance_from_start[starting_vertex] != 0:
				self.breadth_first_search(starting_vertex)

		return self.distance_from_start[ending_vertex]

	def _depth_first_visit(self, starting_vertex):
		self.time += 1
		self.discover_times[starting_vertex] = self.time
		for adjacent_vertex in self.adjacency_map[starting_vertex]:
			# Check for back edges
			# (u,v) is a back edge when discovered but not finished
			if (adjacent_vertex in self.discover_times 
				and adjacent_vertex not in self.finishing_times):
				# (u,v) and (v,u) doesn't not count as a cycle in an udirected graph
				if ((not self.is_directed 
					and self.parents[starting_vertex] != adjacent_vertex)
					or self.is_directed):
					self.back_edges.add((starting_vertex, adjacent_vertex))

			if adjacent_vertex not in self.parents:
				self.parents[adjacent_vertex] = starting_vertex
				self._depth_first_visit(adjacent_vertex)
		self.time += 1
		self.finishing_times[starting_vertex] = self.time

	def depth_first_search(self):
		self.parents = defaultdict(lambda: None)
		self.discover_times = {}
		self.finishing_times = {}
		self.back_edges = set()

		self.time = 0

		for vertex in self.verticies:
			# if vertex not yet visited
			if vertex not in self.parents:
				self.parents[vertex] = None
				self._depth_first_visit(vertex)

	def topological_sort(self):
		# Only works for DAGs
		assert self.is_acyclic, "Must be an acyclic graph to topologically sort"
		assert self.is_directed, "Must be a directed graph to topologically sort"

		# If DFS has not been run yet
		if not self.discover_times:
			self.depth_first_search()

		f_times = list(self.finishing_times.items())
		# Sort by reversed order of finishing times
		f_times.sort(key = lambda pair: pair[1], reverse = True)

		self.sorted_verticies = []
		for vertex, time in f_times:
			self.sorted_verticies.append(vertex)

	def extend(self, verticies=(), edges=()):
		if not verticies and not edges:
			return

		edges = self._convert_set_to_tuples(edges)

		new_verticies = set(verticies)
		new_edges = set(edges)

		self.verticies = self.verticies | new_verticies
		self.edges = self.edges | new_edges

		self._setup_adjacency_map()

		self._reset_attributes()

		self.is_acyclic = self._is_acyclic()

	def _is_acyclic(self):
		self.depth_first_search()

		if self.back_edges:
			return False

		return True

	def _reset_attributes(self):
		"""
		Attributes to be used in various graph methods. All reset to None to be 
		used as a flag to determine whether that method had been called or not. Call
		whenever modifying the graph.
		"""
		self.distance_from_start = None # BFS
		self.discover_times = None # DFS
		self.sorted_verticies = None # Topological sort

	def _convert_set_to_tuples(self, edges):
		# Determine whether edges consists of sets. Assumes all elements in edges
		# are of the same type
		sets = False
		for edge in edges:
			if isinstance(edge, set):
				sets = True
			else:
				sets = False
			break

		# If edges consists of sets, i.e. if building an undirected graph,
		# convert sets to two tuples
		if sets:
			new_edges = []
			for edge in edges:
				assert len(edge) == 2, "All elements in edges must be length 2"
				new_edge = tuple(edge)
				new_edge_2 = tuple(reversed(new_edge))
				new_edges.append(new_edge)
				new_edges.append(new_edge_2)

			edges = new_edges

		return edges

	def _setup_adjacency_map(self):
		self.adjacency_map = defaultdict(set)

		# create adjacency_map, the main representation of the graph
		for edge in self.edges:
			assert len(edge) == 2, "All elements in edges must be length 2"
			assert edge[0] in self.verticies, "Undefined edge: %s" % (edge)
			assert edge[1] in self.verticies, "Undefined edge: %s" % (edge)

			# adjacency map maps every vertex to a set of adjacent verticies
			self.adjacency_map[edge[0]].add(edge[1])

	def __repr__(self):
		return "V: " + str(self.verticies) + " E: " + str(self.edges)

	def __str__(self):
		return str(self.adjacency_map)

class WeightedGraph(Graph):
	"""
	Edges format for each element: (u,v,weight) or ({u,v},weight). 
	Second format gets converted to (u,v,weight) and (v,u,weight)
	"""
	def __init__(self, verticies=(), edges=(), is_directed=False):
		super().__init__(verticies, edges, is_directed)

		self._setup_adjacency_matrix()

	def _convert_set_to_tuples(self, edges):
		for edge in edges:
			if isinstance(edge[0], set):
				sets = True
			else:
				sets = False
			break

		if sets:
			new_edges = []
			for edge, weight in edges:
				assert len(edge) == 2
				# Convertes ({x,y},z) to (x,y,z) and (y,x,z)
				new_edge = tuple(edge)
				new_edge_2 = tuple(reversed(new_edge))
				new_edge += (weight,)
				new_edge_2 += (weight,)
				new_edges.append(new_edge)
				new_edges.append(new_edge_2)

			edges = new_edges

		return edges


	def _setup_adjacency_map(self):
		self.adjacency_map = defaultdict(dict)

		self.negative_edges = False

		for vertex1, vertex2, weight in self.edges:
			assert vertex1 in self.verticies, "Undefined vertex: %s" % (vertex1)
			assert vertex2 in self.verticies, "Undefined vertex: %s" % (vertex2)

			if weight < 0:
				self.negative_edges = True

			self.adjacency_map[vertex1][vertex2] = weight

	def _setup_adjacency_matrix(self):
		self.ordered_verticies = sorted(list(self.verticies))

		self.adjacency_matrix = {}
		for i in range(len(self.verticies)):
			for j in range(len(self.verticies)):
				if i == j:
					self.adjacency_matrix[i,j] = 0
				else:
					self.adjacency_matrix[i,j] = math.inf

		for i, vertex1 in enumerate(self.ordered_verticies):
			for j, vertex2 in enumerate(self.ordered_verticies):
				if vertex2 in self.adjacency_map[vertex1]:
					weight = self.adjacency_map[vertex1][vertex2]
					self.adjacency_matrix[i,j] = weight

	def _reset_attributes(self):
		super()._reset_attributes()
		self.shortest_paths = None
		self.shortest_paths_all = None

	def extend(self, verticies=(), edges=()):
		super().extend(verticies, edges)
		self._setup_adjacency_matrix()

	def shortest_path(self, starting_vertex, ending_vertex):
		assert starting_vertex in self.verticies, \
		"Invalid starting vertex %s" % (starting_vertex)
		assert ending_vertex in self.verticies, \
		"Invalid ending vertex %s" % (ending_vertex)

		# If all pairs shortest paths were calculated
		if self.shortest_paths_all:
			return self.shortest_paths_all[starting_vertex, ending_vertex]

		# If haven't calculated shortest path from starting_vertex before
		if not self.shortest_paths or self.shortest_paths[starting_vertex] != 0:
			self._single_source_shortest_paths(starting_vertex)

		return self.shortest_paths[ending_vertex]

	def all_pairs_shortest_paths(self, johnson=False):
		if not johnson:
			self._floyd_warshall()
		else:
			self._johnson()

	def _floyd_warshall(self):
		n = len(self.verticies)
		d = {}
		d[-1] = self.adjacency_matrix
		for k in range(n):
			d[k] = {}
			for i in range(n):
				for j in range(n):
					d[k][i,j] = min(d[k - 1][i,j], d[k - 1][i,k] + d[k - 1][k,j])

		self.shortest_paths_all = self._convert_to_verticies(d[n - 1])

	def _johnson(self):
		class SourceVertex:
			def __lt__(self, other):
				return True

			def __repr__(self):
				return "SourceVertex"

		# Calculate a new graph that has a new source node connecting to all
		# existing nodes with weight 0. Used to reweight edges

		s = SourceVertex()

		temp_verticies = self.verticies | {s}
		temp_edges = set(i for i in self.edges)
		for vertex in self.verticies:
			temp_edges |= {(s, vertex, 0)}
		temp_graph = WeightedGraph(temp_verticies, temp_edges)

		# Bellman ford on source to detect negative edges and to find shortest
		# paths from source to calculate h function
		temp_graph._initialize_single_source(s)
		try:
			temp_graph._bellman_ford(s)
		except NegativeCycleException:
			raise

		# Function of the vertex that will aid in reweighting
		h = {}
		for vertex in temp_graph.verticies:
			h[vertex] = temp_graph.shortest_path(s, vertex)

		new_weights = {}
		for vertex1, vertex2, weight in temp_graph.edges:
			new_weights[vertex1, vertex2] = weight + h[vertex1] - h[vertex2]

		# Matrix that contains final answer
		d = {}
		for vertex1 in self.verticies:
			self._single_source_shortest_paths(vertex1)
			for vertex2 in self.verticies:
				d[vertex1, vertex2] = self.shortest_path(vertex1, vertex2) - h[vertex1] + h[vertex2]

		self.shortest_paths_all = d

	def _convert_to_verticies(self, d):
		"""Converts a matrix representation back to the given names for the verticies"""
		d_temp = {}
		for i in range(len(self.verticies)):
			for j in range(len(self.verticies)):
				d_temp[self.ordered_verticies[i], self.ordered_verticies[j]] = d[i,j]

		return d_temp

	def _single_source_shortest_paths(self, source):
		self._initialize_single_source(source)
		# is DAG
		if self.is_directed and self.is_acyclic:
			self._DAG_shortest_paths(source)

		elif self.negative_edges:
			try:
				self._bellman_ford(source)
			except NegativeCycleException:
				raise
			finally:
				self.shortest_paths = self._distance_estimates
		else:
			self._dijkstra(source)

		self.shortest_paths = self._distance_estimates

	def _DAG_shortest_paths(self, source):
		# If not already sorted
		if not self.sorted_verticies:
			self.topological_sort()

		for vertex1 in self.sorted_verticies:
			for vertex2, weight in self.adjacency_map[vertex1].items():
				self._relax(vertex1, vertex2, weight)

	def _bellman_ford(self, source):
		for i in range(len(self.verticies) - 1):
			for edge in self.edges:
				self._relax(*edge)

		# If any edges can still be relax, a negative weight cycle exists
		has_negative_cycle = False
		negative_cycle_verticies = set()
		for vertex1, vertex2, weight in self.edges:
			if self._distance_estimates[vertex2] > self._distance_estimates[vertex1] + weight:
				has_negative_cycle = True
				self._distance_estimates[vertex2] = self.NEG_INFINITY
				negative_cycle_verticies.add(vertex2)

		# Adds information if there is a negative cycle
		if has_negative_cycle:
			# Find a vertex that is part of a negative cycle
			for vertex, distance in self._distance_estimates.items():
				if distance != self.NEG_INFINITY:
					continue
				# Set the predecessors of that vertex to -infinity, while loop terminates
				# when the entire cycle is set to -infinity; i.e. predecessor is also
				# -infinity. Also adds each vertex of cycle to negative_cycle_verticies
				while self._distance_estimates[self.parents[vertex]] != self.NEG_INFINITY:
					vertex = self.parents[vertex]
					negative_cycle_verticies.add(vertex)
					self._distance_estimates[vertex] = self.NEG_INFINITY

				break

		if has_negative_cycle:
			raise NegativeCycleException(negative_cycle_verticies)

	def _dijkstra(self, source):
		# Reverse dict.items so it is compared by value (weights)
		to_be_processed = heap(item for item in self._distance_estimates.items())
		while to_be_processed:
			# Extract vertex with the minimum estimated distance
			vertex = to_be_processed.extract_min()
			for adjacent_vertex, weight in self.adjacency_map[vertex].items():
				self._relax(vertex, adjacent_vertex, weight, to_be_processed)

	def _initialize_single_source(self, source):
		self.INFINITY = math.inf
		self.NEG_INFINITY = -math.inf
		self._distance_estimates = defaultdict(lambda: self.INFINITY)
		self.parents = defaultdict(lambda: None)

		for vertex in self.verticies:
			self._distance_estimates[vertex] = self.INFINITY
			self.parents[vertex] = None

		self._distance_estimates[source] = 0

	def _relax(self, vertex1, vertex2, weight, update_keys=None):
		if self._distance_estimates[vertex2] > self._distance_estimates[vertex1] + weight:
			self._distance_estimates[vertex2] = self._distance_estimates[vertex1] + weight
			# Decrease key
			if update_keys:
				update_keys[vertex2] = self._distance_estimates[vertex2]
			self.parents[vertex2] = vertex1

	def kruskal(self):
		A = set()
		D = DisjointSet()
		for vertex in self.verticies:
			D.new_set(vertex)
		sorted_edges = sorted(self.edges, key=lambda edge: edge[2])
		for vertex1, vertex2, weight in sorted_edges:
			v1 = D.find(vertex1)
			v2 = D.find(vertex2)
			# Not in same connected component
			if v1 != v2:
				A |= {(vertex1, vertex2, weight)}
				D.union(v1, v2)
		return A

	def prim(self, source):
		assert source in self.verticies

		distances = {}
		self.MST_parents = {}
		for vertex in self.verticies:	
			distances[vertex] = math.inf
			self.MST_parents[vertex] = None
		distances[source] = 0
		to_be_processed = heap(item for item in distances.items())
		while to_be_processed:
			vertex = to_be_processed.extract_min()
			for adjacent_vertex in self.adjacency_map[vertex]:
				weight = self.adjacency_map[vertex][adjacent_vertex]
				if adjacent_vertex in to_be_processed and weight < distances[adjacent_vertex]:
					self.MST_parents[adjacent_vertex] = vertex
					distances[adjacent_vertex] = weight
					to_be_processed[adjacent_vertex] = weight

class FlowNetwork(Graph):
	def __init__(self, verticies=(), edges=(), source=None, sink=None):
		"""
		edges - (vertex1, vertex2, capacity)
		source, sink - can be an iterable for multiple sources/sinks
		"""
		self.verticies = set(verticies)
		self.edges = set(edges)

		self._setup_adjacency_map()

		self._setup_network(source, sink)

		self._reset_attributes()

		self.flow = {}

	def _setup_adjacency_map(self):
		self.adjacency_map = defaultdict(dict)

		for vertex1, vertex2, capacity in self.edges:
			assert vertex1 in self.verticies, "Undefined vertex: %s" % (vertex1)
			assert vertex2 in self.verticies, "Undefined vertex: %s" % (vertex2)
			assert capacity >= 0, "Capacity must be positive"

			self.adjacency_map[vertex1][vertex2] = capacity

	def _setup_network(self, source, sink):
		#### ALSO FIX ANTI-PARALLEL EDGES #####

		class Sentinel:
			def __init__(self, type='source'):
				self.type = type
				self._sentinel_class = True

			def __repr__(self):
				return "super" + self.type

		try:
			iter(source)
		except TypeError:
			assert source in self.verticies
			self.source = source
		else:
			supersource = Sentinel()
			self.verticies.add(supersource)
			for s in source:
				assert source in self.verticies
				self.adjacency_map[supersource][s] = math.inf
			self.source = supersource

		try:
			iter(sink)
		except TypeError:
			assert sink in self.verticies
			self.sink = sink
		else:
			supersink = Sentinel("sink")
			self.verticies.add(supersink)
			for t in sink:
				assert sink in self.verticies
				self.adjacency_map[s][supersource] = math.inf
			self.sink = supersink

	def max_flow(self):
		self._edmonds_karp()

		max_flow = 0
		# One source
		if not hasattr(self.source, '_sentinel_class'):
			for vertex in self.adjacency_map[self.source]:
				max_flow += self.flow[self.source, vertex]

		# Multiple sources
		else:
			for subsource in self.adjacency_map[self.source]:
				for vertex in self.adjacency_map[subsource]:
					# If not a another subsource
					if vertex not in self.adjacency_map[self.source]:
						max_flow += self.flow[subsource, vertex]

		return max_flow

	def _edmonds_karp(self):
		for vertex1, vertex2, capacity in self.edges:
			self.flow[vertex1, vertex2] = 0
		
		while True:
			residual_network = self._construct_residual_network()
			try:
				residual_capacity = self._find_augmenting_path(residual_network)
			except NoPathFound:
				break

			for vertex1, vertex2 in self.residual_path:
				if vertex2 in self.adjacency_map[vertex1]:
					self.flow[vertex1, vertex2] += residual_capacity
				else:
					self.flow[vertex2, vertex1] -= residual_capacity

	def _construct_residual_network(self):
		residual_edges = set()
		
		for vertex1 in self.verticies:
			for vertex2, capacity in self.adjacency_map[vertex1].items():
				flow = self.flow[vertex1, vertex2]
				if flow < capacity:
					residual_edges.add((vertex1, vertex2, capacity - flow))
				if flow > 0:
					residual_edges.add((vertex2, vertex1, flow))

		return FlowNetwork(self.verticies, residual_edges, self.source, self.sink)

	def _find_augmenting_path(self, residual_network):
		residual_network.breadth_first_search(self.source)

		if not residual_network.parents[self.sink]:
			raise NoPathFound
		else:
			curr_node = self.sink
			prev_node = residual_network.parents[self.sink]

		residual_capacity = math.inf
		self.residual_path = set()
		while prev_node:
			edge_capacity = residual_network.adjacency_map[prev_node][curr_node]
			if edge_capacity < residual_capacity:
				residual_capacity = edge_capacity
			self.residual_path.add((prev_node, curr_node))
			curr_node = prev_node
			prev_node = residual_network.parents[curr_node]

		return residual_capacity


#V = [1,2,3,4,5,6,7,8,9,10,11]
#E = [{1,2},{3,4},{1,5},{4,5},{2,10},{5,7},{5,8},{7,9},{8,9},{2,3},{7,10}]

#new_V = [15,16,17]
#new_E = [{4,6},{6,15},{15,17},{17,11}]

#DAG
#V = [1,2,3,4,5,6]
#E = [(1,2,1),(1,3,3),(2,3,3),(2,4,2),(3,4,10),(3,6,4),(4,5,1),(4,6,2),(5,6,2)]

#HARDCORE TEST
#V = [0,1,2,3,4,5,6,7,8,9,10]
#E = [(0,1,1),(0,2,7),(0,3,6),(2,4,2),(2,3,1),(1,4,8),(1,5,3),(3,4,2),(4,7,7),(4,9,5),
#(5,2,1),(5,8,9),(6,5,4),(6,7,3),(3,6,2),(7,9,2),(7,1,2),(8,10,4),(9,10,2),(9,3,0)]
# 0 - 10: 10

#General Graph (All-pairs shortest paths)
#V = [1,2,3,4,5]
#E = [(1,3,4),(1,4,3),(2,1,2),(3,2,6),(3,5,5),(4,2,4),(4,5,3),(4,3,5),(5,2,2),(5,1,1)]

#Undirected Graph (MST)
#V = ['a','b','c','d','e','f','g','h','i']
#E = [({'a','b'},4),({'a','h'},8),({'b','c'},8),({'b','h'},11),({'c','d'},7),({'c','f'},4),
#({'c','i'},2),({'d','f'},14),({'d','e'},9),({'e','f'},10),({'f','g'},2),({'g','h'},1),({'g','i'},6),
#({'h','i'},7)]
"""
# Flow network
V = [1,2,3,4,5,6]
E = [(1,2,16),(1,3,13),(2,4,12),(3,2,4),(3,5,14),(4,3,9),(4,6,20),(5,4,7),(5,6,4)]

G = FlowNetwork(V, E, source=1, sink=6)

print(G.max_flow())
"""

from itertools import product
V = [s for s in product('abcdefghijklmnopqrstuvwxyz','abcdefghijklmnopqrstuvwxyz',
	'abcdefghijklmnopqrstuvwxyz','abcdefghijklmnopqrstuvwxyz')]
E = []
for s in V:
	if 

G = Graph(V, E)