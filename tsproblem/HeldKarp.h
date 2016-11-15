#ifndef HELD_KARP
#define HELD_KARP

#include <iostream>
#include <vector>
#include <utility>
#include <map>
#include <fstream>
#include <string>
#include <climits>
#include <sstream>
#include <cstdlib>
#include <chrono>

using namespace std;
using namespace std::chrono;

class HeldKarp {
	private:
		vector<vector <int> > c;
		vector<int> m_path;
		int m_cost;
		map<pair<int, vector<int> >, pair<vector<int>, int> >  previous;
		pair<vector<int>, int> held_karp(int v, vector<int> s);
	public:
		HeldKarp(vector<vector <int> > c, int v);
		vector<int> path(){
			return m_path;
		}
		int cost(){
			return m_cost;
		}

};

#endif
