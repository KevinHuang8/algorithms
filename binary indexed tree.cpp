template <typename T>
struct BinaryIndexedTree {
	vector<T> values;
	vector<T> tree;

	BinaryIndexedTree(int size) : values(size), tree(size) {}

	BinaryIndexedTree(vector<T>& v) : values(v), tree(v.size() + 1) {
		vector<T> temp = values;
		for (int i = 0; i < values.size(); ++i) {
			update(i, values[i]);
		}
		values = temp;
	}
	//return sum of values[0...index] inclusive
	T prefix_sum(int index) {
		T sum = 0;
		index += 1;
		while (index > 0) {
			sum += tree[index];
			//parent
			index = index - (index & -index);
		}
		return sum;
	}

	void update(int index, T val) {
		values[index] += val;
		index += 1;
		while (index <= values.size()) {
			tree[index] += val;
			index = index + (index & -index);
		}
	}

	//returns sum of values[a...b], inclusive
	T sum_between(int a, int b) {
		if (a == 0)
			return prefix_sum(b);
		else if (b == 0)
			return prefix_sum(a);
		else if (a > b)
			return prefix_sum(a) - prefix_sum(b - 1);
		else
			return prefix_sum(b) - prefix_sum(a - 1);
	}
};