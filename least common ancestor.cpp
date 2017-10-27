//needs sparse table
//solves by converting LCA to RMQ
//O(nlogn) pre-processing, O(1) queries
template <typename T>
struct LCA {
	unordered_map<T, vector<T>> child;
	vector<T> walk;
	vector<int> depths;
	SparseTable<int> s;
	unordered_map<T, int> first_occurence;
	
	LCA(unordered_map<T, vector<T>> &c) : child(c) {}

	LCA() {}

	//call this after setting up the tree but before any queries
	void initialize(T root) {
		dfs(root, 0);
		s = SparseTable<int>(depths);
	}

	void add_node(T key, T value) {
		if (child.find(key) == child.end()) {
			vector<T> v;
			child[key] = v;
		}
		child[key].push_back(value);
	}

	void dfs(T node, int depth) {
		if (first_occurence.find(node) == first_occurence.end()) {
			first_occurence[node] = walk.size();
		}
		walk.push_back(node);
		depths.push_back(depth);
		for (T v : child[node]) {
			dfs(v, depth + 1);
			walk.push_back(node);
			depths.push_back(depth);
		}
	}

	T query(T a, T b) {
		if (first_occurence[a] > first_occurence[b])
			return walk[s.RMQ(first_occurence[b], first_occurence[a])];
		return walk[s.RMQ(first_occurence[a], first_occurence[b])];
	}
};