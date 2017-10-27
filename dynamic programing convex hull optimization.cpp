/*
Dynamic programming convex hull optimization: https://wcipeg.com/wiki/Convex_hull_trick
Note: has little to do with convex hull algorithms

Assumes that lines will be added in order of decreasing slope for min and increasing slope for max
Assumes query values will be non-decreasing or non-increasing (use corresponding query)
*/
struct ConvexHullOptimizer {
	//implemented as a stack of pairs<m, b>
	vector<pair<long long, long long>> lines;
	vector<double> intervals;
	//if query values are non-decreasing, use 0, if they are non-increasing, use INF
	long long prev_query = 0;
	//represents top of the stack
	long long top = -1;

	ConvexHullOptimizer(long long size) : lines(size), intervals(size) {}

	void add_line(long long m, long long b) {
		if (top >= 1) {
			//while intersection of new line with second to last line is left of the intersection of 
			//the second to last line with the last line
			while (top >= 1 && line_intersection(m, b, lines[top - 1].first, lines[top - 1].second)
				< line_intersection(lines[top - 1].first, lines[top - 1].second, lines[top].first, lines[top].second))
				//last line becomes irrelevant, pop it off the stack
				--top;

			lines[top + 1] = make_pair(m, b);
			intervals[top] = line_intersection(m, b, lines[top].first, lines[top].second);
			++top;

		}
		else if (top == 0) {
			lines[top + 1] = make_pair(m, b);
			intervals[top] = line_intersection(m, b, lines[top].first, lines[top].second);
			++top;
		}
		else if (top == -1) {
			lines[top + 1] = make_pair(m, b);
			++top;
		}
	}

	//non-decreasing version
	long long queryincreasing(long long x) {
		for (long long i = prev_query; i <= top; ++i) {
			if (i == 0) {
				if (top == 0)
					return lines[0].first * x + lines[0].second;
				else if (x < intervals[0]) {
					prev_query = i;
					return lines[0].first * x + lines[0].second;
				}
			}
			else if (i == top) {
				if (x > intervals[top])
					prev_query = i;
				return lines[top].first * x + lines[top].second;
			}
			else if (x > intervals[i - 1] && x < intervals[i]) {
				prev_query = i;
				return lines[i].first * x + lines[i].second;
			}
		}
	}

	//non-increasing version
	int querydecreasing(int x) {
		for (int i = prev_query; i >= 0; --i) {
			if (prev_query == INF)
				prev_query = top;
			if (i == 0 && top == 0)
				return lines[0].first * x + lines[0].second;
			else if (i == 0 && x < intervals[0]) {
				prev_query = i;
				return lines[0].first * x + lines[0].second;
			}
			else if (i == top && x > intervals[top]) {
				prev_query = i;
				return lines[top].first * x + lines[top].second;
			}
			else if (x > intervals[i - 1] && x < intervals[i]) {
				prev_query = i;
				return lines[i].first * x + lines[i].second;
			}
		}
	}

	double line_intersection(long long m1, long long b1, long long m2, long long b2) {
		return (b1 - b2) / (double)(-m1 + m2);
	}
};
