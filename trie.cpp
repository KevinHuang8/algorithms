//max size = O(N*M) where N is number of words and M is length of longest word
#define MAX 2000
#define ALPHABET_SIZE 26
#define FIRST_LETTER 'A'
#include <cstring>
struct trie {
	long long tree[MAX][ALPHABET_SIZE + 1] = { 0 };
	bool is_word[MAX];
	long long prefixes[MAX] = { 0 };
	long long counter = 1;

	void insert(string s) {
		//ensure no duplicates
		//if (contains(s))
		//	return;

		long long curr_node = 0;
		for (int i = 0; i < s.length(); ++i) {
			char c = s[i];

			if (tree[curr_node][c - FIRST_LETTER] == 0) {
				tree[curr_node][c - FIRST_LETTER] = counter;
				++counter;
			}

			++prefixes[curr_node];
			curr_node = tree[curr_node][c - FIRST_LETTER];

			if (i == s.length() - 1)
				is_word[curr_node] = true;
		}
	}

	void insert(vector<string> words) {
		for (string word : words)
			insert(word);
	}

	bool contains(string s) {
		long long curr_node = 0;
		for (char c : s) {
			if (tree[curr_node][c - FIRST_LETTER] == 0)
				return false;
			curr_node = tree[curr_node][c - FIRST_LETTER];
		}
		return is_word[curr_node];
	}

	//number of words with 'prefix' as a prefix
	long long count_prefixes(string prefix) {
		long long curr_node = 0;
		for (char c : prefix) {
			if (tree[curr_node][c - FIRST_LETTER] == 0)
				return 0;
			curr_node = tree[curr_node][c - FIRST_LETTER];
		}
		return prefixes[curr_node];
	}

	void clear() {
		memset(tree, 0, sizeof(tree));
		memset(is_word, 0, sizeof(is_word));
		memset(prefixes, 0, sizeof(prefixes));
		counter = 1;
	}
};