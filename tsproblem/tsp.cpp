#include <iostream>
#include <vector>
#include <utility>
#include <map>
#include <fstream>
#include <string>
#include <climits>
#include <sstream>
#include <cstdlib>
using namespace std;

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

pair<vector<pair<int, int> >, int> held_karp(vector<vector<int> > c, int v, vector<int> s, map<pair<int, vector<int> >, pair<vector<pair<int, int> >, int> >& previous)
{
    vector<pair<int, int> > path;
    if (s.size() == 0) {
        path.push_back(make_pair(0,v));
        return make_pair(path, c[0][v]);
    }
    int min = INT_MAX;
    int cost = 0;
    for (int i = 0; i < s.size(); i++) {
        vector<int> new_s;
	int u = s[i];
        for (int j = 0; j < s.size(); j++) {
            if (i != j) {
                new_s.push_back(s[j]);
            }
        }
        pair<vector<pair<int, int> >, int> path_cost;
	pair<int, vector<int> > u_new_s_pair = make_pair(u,new_s);
        if (previous.count(u_new_s_pair) != 0) {
            path_cost = previous[u_new_s_pair];
        }
        else {
            path_cost = held_karp(c, u, new_s, previous);
            previous[u_new_s_pair] = path_cost;
        }
        cost = c[u][v] + path_cost.second;
        if (cost < min) {
	    path = vector<pair<int, int> >();
            path = path_cost.first;
            path.push_back(make_pair(u, v));
            min = cost;
        }
    }
    return make_pair(path, min);
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
{	for(int i = 1; i < argc; i++){
		vector< vector<int> > m = loadMatrix(argv[i]);
		cout << "size = " << m.size() << endl;
		cout << endl;
		for(int j = 0; j < m.size(); j++){
			for(int k = 0; k < m.size(); k++){
				cout << m[j][k] << " ";
			}
			cout << endl;
		}
		cout << endl;
		vector<int> s;
		for(int j = 1; j < m.size(); j++){
			s.push_back(j);
		}
		map<pair<int, vector<int> >, pair<vector<pair<int, int> >, int> >  previous;
		pair<vector<pair<int, int> >, int> result = held_karp(m,0,s,previous);
		vector<pair<int, int> > path = result.first;
		cout << "path: " << endl;
		for(int j = 0; j < path.size(); j++){
			cout << path[j].first + 1 << endl;
		}
		cout << path[path.size()-1].second + 1 << endl;
		cout << endl;
		cout << "cost: " << result.second << endl; 
	}
}




