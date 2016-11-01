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

int main()
{

    ifstream file("p01.tsp");
    string line;
    int k = 0;
    vector<vector<int> > c;
    while (getline(file, line)) {
        if (line == "EDGE_WEIGHT_SECTION") {
            while (getline(file, line) && k < 15) {
               vector<string> row_str = split(line, ' ');
               vector<int> row;
                for (int i = 0; i < row_str.size(); i++) {
                    if (row_str[i] != "") {
                        row.push_back(atoi(row_str[i].c_str()));
                    }
                }
                for (int j = 0; j < row.size(); j++) {
                    cout << row[j] << " ";
                }
                c.push_back(row);
                k++;
                cout << endl;
            }
        }
    }
    vector<int> s;
    for (int i = 1; i < 15; i++) {
        s.push_back(i);
    }
    map<pair<int, vector<int> >, pair<vector<pair<int, int> >, int> > previous;

pair<vector<pair<int, int> >, int> path_cost = held_karp(c, 0, s, previous);
   cout << "path: " << endl;

    for (int i = 0; i < path_cost.first.size(); i++) {
        cout << path_cost.first[i].first << "-> " << path_cost.first[i].second << " : " << c[path_cost.first[i].first][path_cost.first[i].second] << endl;
    }

    cout << "cost:" << path_cost.second << endl;
    cout << "path from file: " << endl;

    vector<int> p;
    p.push_back(1);
    p.push_back(13);
    p.push_back(2);
    p.push_back(15);
    p.push_back(9);
    p.push_back(5);
    p.push_back(7);
    p.push_back(3);
    p.push_back(12);
    p.push_back(14);
    p.push_back(10);
    p.push_back(8);
    p.push_back(6);
    p.push_back(4);
    p.push_back(11);
    p.push_back(1);

    for (int j = 0; j < p.size(); j++) {
        p[j] -= 1;
    }
    int tt = 0;
    for (int j = 0; j < p.size(); j++) {
        cout << p[j] << "-> " << p[j + 1] << " : " << c[p[j]][p[j + 1]] << endl;
        tt += c[p[j]][p[j + 1]];
    }
    cout << "cost from file: " << tt << endl;

}
