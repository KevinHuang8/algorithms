/*
Assumes Heap class
Assumes global variables:
dist[] - key: T value: int
adjacency_list[] - key: T, value: vector<T>
weight[][] - key: T, T value: int
optional: distances[][] - shortest path from a to b
useful for multiple dijkstra runs from different sources
*/
template <typename T>
void dijkstra(vector<T> node_list, T source) {
	vector<pair<int, T>> v;
	for (int i = 0; i < node_list.size(); ++i) {
		T val = node_list[i];
		if (val == source) {
			dist[source] = 0;
			//distances[source][source] = 0;
			v.push_back(make_pair(0, source));
			continue;
		}
		dist[val] = 2100000000;
		v.push_back(make_pair(dist[val], val));
	}

	Heap<pair<int, T>> to_process(v);
	while (!to_process.empty()) {
		pair<int, T> node = to_process.extract_min();
		for (T adj : adjacency_list[node.second]) {
			if (dist[adj] > dist[node.second] + weight[node.second][adj]) {
				to_process.decrease_key(make_pair(dist[adj], adj), make_pair(dist[node.second] + weight[node.second][adj], adj));
				dist[adj] = dist[node.second] + weight[node.second][adj];
				//distances[source][adj] = dist[adj];
			}
		}
	}
}