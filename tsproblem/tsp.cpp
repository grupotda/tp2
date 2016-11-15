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
#include "HeldKarp.h"

using namespace std;
using namespace std::chrono;

void split(const string& s, char delim, vector<string>& elems)
{
    stringstream ss;
    ss.str(s);
    string item;
    while (getline(ss, item, delim)) {
        elems.push_back(item);
    }
}

vector<string> split(const string& s, char delim)
{
    vector<string> elems;
    split(s, delim, elems);
    return elems;
}

vector < vector <int > > loadMatrix(char* filename){
		ifstream file(filename);
		string row;
		vector< vector<int> > m;
		int i = 0;
		while(getline(file,row)){
			vector<string> row_str = split(row,' ');
			m.push_back(vector<int>());
			for(int j = 0; j < row_str.size(); j++){
					m[i].push_back(atoi(row_str[j].c_str()));
			}
			i++;
		}
	return m;
}

int main(int argc, char* argv[])
{	

for(int i = 1; i < argc; i++){
		cout << " - " << argv[i] << " - "<< endl;
		vector< vector<int> > m = loadMatrix(argv[i]);
		vector<int> s;
		for(int j = 1; j < m.size(); j++){
			s.push_back(j);
		}
		high_resolution_clock::time_point t1 = high_resolution_clock::now();
		HeldKarp hk (m,0);
		vector< pair < int, int> > path = hk.path();
		int cost = hk.cost();
		cout << "cost is: " << cost << endl;
		high_resolution_clock::time_point t2 = high_resolution_clock::now();
		auto duration = duration_cast<milliseconds>( t2 - t1 ).count();

		cout << duration << std::endl;

//		vector<pair<int, int> > path = result.first;
		//cout << "path: " << endl;
//		for(int j = 0; j < path.size(); j++){
//			cout << path[j].first + 1 << endl;
//		}
//		cout << path[path.size()-1].second + 1 << endl;
//		cout << endl;
//		cout << "cost: " << result.second << endl; 
	}
}




