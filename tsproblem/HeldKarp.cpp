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


vector<int> remove_from(vector<int> s, int u) {
    vector<int> new_s;
    for (int j = 0; j < s.size(); j++) {
        if (u != s[j]) {
            new_s.push_back(s[j]);
        }
    }
    return new_s;
}

HeldKarp::HeldKarp(vector<vector<int> > c, int v) {
    //Acá restamos uno, para que el índice 0 corresponda al vértice 1, el 1 al 2, etc...
    v = v - 1;
    vector<int> s;
    for (int j = 0; j < c.size(); j++) {
        if (j != v) {
            s.push_back(j);
        }
    }
    this->c = c;
    pair<vector<int>, int> path_cost = held_karp(v, s);
    this->m_path = path_cost.first;
    //Sumamos uno a cada vértice para que nos dé la solución como queremos
    for (int j = 0; j < m_path.size(); j++) {
        m_path[j]++;
    }
    this->m_cost = path_cost.second;
}

pair<vector<int>, int> HeldKarp::held_karp(int v, vector<int> s) {
    vector<int> path;

    // Si S = {}, el camino es sólo la arista desde el origen (el 0) a este vértice
    if (s.size() == 0) {
        path.push_back(0);
        path.push_back(v);
        return make_pair(path, c[0][v]);
    }
    int min = INT_MAX;
    int cost = 0;
    for (int i = 0; i < s.size(); i++) {
        // Para cada u en S

        int u = s[i];

        // Armamos S - {u}
        vector<int> new_s = remove_from(s, u);

        pair<vector<int>, int> path_cost;

        pair<int, vector<int> > u_new_s_pair = make_pair(u, new_s);

        if (previous.count(u_new_s_pair) != 0) {
            // Si ya estaba calculado, no lo calculamos otra vez
            path_cost = previous[u_new_s_pair];
        }
        else {
            // Si no estaba calculado...
            path_cost = held_karp(u, new_s);
            previous[u_new_s_pair] = path_cost;
        }

        // Costo total = costo hasta u + costo desde u hasta este vértice
        cost = path_cost.second + c[u][v];

        if (cost < min) {
            // Nos quedamos con el mínimo
            // Agregamos el camino hasta u
            path = path_cost.first;
            // Y la arista desde u hasta este vértice
            path.push_back(v);
            min = cost;
        }
    }
    // Devolvemos el camino y el costo total
    return make_pair(path, min);
}

