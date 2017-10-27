template <typename T>
struct SparseTable {
	vector<vector<T>> table;
	vector<T> A;

	SparseTable(vector<T> A) {
		this->A = A;
		table.resize(A.size());
		for (int i = 0; i < table.size(); ++i)
			table[i] = vector<T>(ceil(log2(table.size())));

		for (int i = 0; i < table.size(); ++i)
			table[i][0] = i;
		for (int j = 1; (1 << j) <= table.size(); ++j) {
			for (int i = 0; i + (1 << j) - 1 < table.size(); ++i) {
				if (A[table[i][j - 1]] < A[table[i + (1 << (j - 1))][j - 1]])
					table[i][j] = table[i][j - 1];
				else
					table[i][j] = table[i + (1 << (j - 1))][j - 1];
			}
		}
	}

	//RMQ(i, j) returns index of min element in interval [i, j] inclusive. Note it returns index, not value
	int RMQ(int i, int j) {
		int k = log2(j - i + 1);
		if (A[table[i][k]] < A[table[j - (1 << k) + 1][k]])
			return table[i][k];
		return table[j - (1 << k) + 1][k];
	}
};