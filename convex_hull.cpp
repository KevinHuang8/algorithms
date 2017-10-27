//euclidean distance between point a and b
double distance(pair<double, double> a, pair<double, double> b) {
	return sqrt(pow((a.first - b.first), 2) + pow((a.second - b.second), 2));
}

//computes PQ X PR
//1 = R is counterclockwise to Q with respect to P, -1 = counterclockwise, 0 = same
int orientation(pair<double, double> p, pair<double, double> q, pair<double, double> r) {
	double cross_product = (q.first - p.first) * (r.second - p.second) - (r.first - p.first) * (q.second - p.second);
	if (cross_product == 0)
		return 0;
	else if (cross_product > 0)
		return 1;
	else
		return -1;
}

vector<pair<double, double>> points;
vector<pair<double, double>> hull;

void convex_hull(pair<double, double> initial_point) {
	auto p = initial_point;
	pair<double, double> endpoint = initial_point;
	do {
		hull.push_back(p);
		//endpoint = possible next point on the convex hull
		endpoint = points[0];
		//search through all possible next points
		for (auto point : points) {
			//find the most counterclockwise point, if tied, take the farthest away
			if (orientation(p, endpoint, point) == 1)
				endpoint = point;
			else if (orientation(p, endpoint, point) == 0) {
				if (distance(p, point) > distance(p, endpoint))
					endpoint = point;
			}
		}
		p = endpoint;
	} while (p != initial_point);
}
