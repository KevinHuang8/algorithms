template <typename V>
struct node {
	int low;
	int high;
	V val;
	V lazy;
	node() {}
	node(int lo, int hi, V v) : low(lo), high(hi), val(v), lazy() {}
};

template <typename V>
class SegmentTree {
private:
	vector<node<V>> nodes;
	vector<V> elements;

	void build_tree(int index, int low, int high) {
		if (low == high) {
			nodes[index] = node<V>(low, high, elements[low]);
			return;
		}

		int leftchild = 2 * index + 1;
		int rightchild = 2 * index + 2;
		int mid = (low + high) / 2;
		build_tree(leftchild, low, mid);
		build_tree(rightchild, mid + 1, high);
		nodes[index] = merge(nodes[leftchild], nodes[rightchild]);
	}

	//get node responsible for segment [start, end]. Start search from node[index]
	node<V> query_node(int index, int start, int end) {
		node<V> n = nodes[index];

		if (start == n.low && end == n.high)
			return n;

		int mid = (n.low + n.high) / 2;

		//if the required interval is completely to the left or completely to the right
		if (start > mid)
			return query_node(2 * index + 2, start, end);
		if (end <= mid)
			return query_node(2 * index + 1, start, end);

		return merge(query_node(2 * index + 1, start, mid), query_node(2 * index + 2, mid + 1, end));
	}

	void update(int node_index, int index, V new_val) {
		node<V> &n = nodes[node_index];

		//is leaf node
		if (n.low == n.high) {
			change_value(n, new_val);
			return;
		}

		int mid = (n.low + n.high) / 2;
		int leftchild = 2 * node_index + 1;
		int rightchild = 2 * node_index + 2;
		//binary search for the leaf containing the index
		if (index <= mid)
			update(leftchild, index, new_val);
		else
			update(rightchild, index, new_val);

		//propagate updates upward
		n = merge(nodes[leftchild], nodes[rightchild]);
	}

	void range_update(int index, int start, int end, V new_val) {
		node<V> &n = nodes[index];

		//Resolve pending lazy updates:
		if (is_lazy(n)) {
			apply_lazy(n, n.lazy);

			//if not a leaf, delay further updates to children
			/*ADD UPDATE*/
			if (n.high != n.low) {
				nodes[2 * index + 1].lazy += n.lazy;
				nodes[2 * index + 2].lazy += n.lazy;
			}

			n.lazy = 0;
		}

		//if segment is contained entirely within the update range, you don't need to go
		//further into the tree for now, b/c the update will apply to everything in that segment
		//Do not propagate:
		/*CONDITION FOR NO PROPAGATION*/
		if (n.low >= start && n.high <= end) {
			//update current segment
			apply_lazy(n, new_val);

			/*ADD UPDATE*/
			if (n.high != n.low) {
				nodes[2 * index + 1].lazy += new_val;
				nodes[2 * index + 2].lazy += new_val;
			}
			return;
		}

		//Propagate:
		int mid = (n.high + n.low) / 2;
		int rightchild = 2 * index + 2;
		int leftchild = 2 * index + 1;
		if (start > mid) {
			range_update(rightchild, start, end, new_val);
			range_update(leftchild, start, mid, new_val); // just to update lazy
		}
		else if (end <= mid) {
			range_update(leftchild, start, end, new_val);
			range_update(rightchild, mid + 1, end, new_val); //just to update lazy
		}
		else {
			range_update(leftchild, start, mid, new_val);
			range_update(rightchild, mid + 1, end, new_val);
		}

		n = merge(nodes[leftchild], nodes[rightchild]);
	}

	node<V> lazy_query_node(int index, int start, int end) {
		node<V> &n = nodes[index];

		//Resolve pending lazy updates
		if (is_lazy(n)) {
			/*Apply lazy update, implementation defined*/
			apply_lazy(n, n.lazy);

			//if not a leaf, delay further updates to children
			/*ADD UPDATE*/
			if (n.high != n.low) {
				nodes[2 * index + 1].lazy += n.lazy;
				nodes[2 * index + 2].lazy += n.lazy;
			}

			n.lazy = 0;
		}

		//if segment is contained entirely within the search range
		//You can just return the index without going further into the tree, b/c the
		//query will include the entire segment
		//Do not propagate:
		/*CONDITION FOR NO PROPAGATION*/
		if (n.low >= start && n.high <= end)
			return nodes[index];

		//propagate:
		int mid = (n.low + n.high) / 2;
		if (start > mid)
			return lazy_query_node(2 * index + 2, start, end);
		if (end <= mid)
			return lazy_query_node(2 * index + 1, start, end);

		return merge(lazy_query_node(2 * index + 1, start, mid), lazy_query_node(2 * index + 2, mid + 1, end));
	}

	/*
	Implementation Defined Methods
	*/

	//whether node n has a lazy update queued
	bool is_lazy(node<V> &n) {
		return n.lazy != 0;
	}

	//obtain value of combined segment from left subsegment and right subsegment
	node<V> merge(node<V> left, node<V> right) {
		//depends on what value you are storing
		node<V> new_node(left.low, right.high, left.val + right.val);
		return new_node;
	}

	//applies update_val to the segment controlled by n
	void apply_lazy(node<V> &n, V update_val) {
		n.val += (n.high - n.low + 1)*update_val;
	}

	//update the value in node n by new_val
	void change_value(node<V> &n, V new_val) {
		n.val = new_val;
	}

	//is propagation required condition
	bool propagate() {}

	//how to add a lazy update to the lazy queue
	void add_update() {}

	/*
	Implementation Defined Methods
	*/

public:
	SegmentTree(vector<V> v) {
		int p = 1;
		while (pow(2, p) < v.size())
			++p;
		nodes.resize(pow(2, p + 1));
		elements = v;
		build_tree(0, 0, elements.size() - 1);
	}

	//return value of segment [left, right] inclusive
	V query(int start, int end) {
		return query_node(0, start, end).val;
	}

	//updates value at index with new_val
	void update(int index, V new_val) {
		update(0, index, new_val);
	}

	//return value of segment [left, right] inclusive. Must be used with lazy updating
	V lazy_query(int start, int end) {
		return lazy_query_node(0, start, end).val;
	}

	//updates all values in [start, end] inclusive with new_val. Lazy
	void range_update(int start, int end, V new_val) {
		range_update(0, start, end, new_val);
	}
};