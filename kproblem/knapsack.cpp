#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>
#include <sstream>
#include <chrono>
using namespace std;
using namespace std::chrono;

int knapsack(int capacity, const std::vector<int>& values, const std::vector<int>& weights){
	std::vector<int> m_prev (capacity + 1, 0);
	std::vector<int> m_curr (capacity + 1, 0);
//	std::vector< std::vector<int> > n (values.size(), std::vector<int>(capacity + 1, 0));
	for(int i = 0; i < values.size(); i++){
		for(int j = 1; j < capacity + 1; j++){
			if (weights[i] > j){
				m_curr[j] = m_prev[j];
//				n[i][j] = 0;
			} else {
				if(m_prev[j-weights[i]] + values[i] >= m_prev[j]){
				m_curr[j] = m_prev[j - weights[i]] + values[i];
//				n[i][j] = 1;
				} else {
					m_curr[j] = m_prev[j];
//					n[i][j] = 0;
				}
			}
		}
		m_prev = m_curr;
		m_curr = std::vector<int> (capacity + 1, 0);
	}
	int j = capacity;
	std::vector<int> present (values.size(), 0);
	int z = 0;
//	for(int i = values.size() - 1; i >= 0; i--){
//		present[i] = n[i][j];
//		z += present[i] * values[i];
//		if(present[i]){
//			j -= weights[i];
//		}
//	}
//	return z;
	return m_prev[j];
}
void split(const std::string &s, char delim, std::vector<std::string> &elems) {
	    std::stringstream ss;
	        ss.str(s);
		    std::string item;
		        while (std::getline(ss, item, delim)) {
				        elems.push_back(item);
					    }
}
std::vector<std::string> split(const std::string &s, char delim) {
	    std::vector<std::string> elems;
	        split(s, delim, elems);
		    return elems;
}

void testFile(std::string filename){
	std::cout << "FILE: " << filename << std::endl;
	std::ifstream file(filename.c_str());
	int ok = 0;
	for(int i = 0; i < 100; i++){
	    	high_resolution_clock::time_point t1 = high_resolution_clock::now();
		int capacity = 0;
		std::vector<int> values;
		std::vector<int> weights;
		std::string s;
		int n = 0;
		std::getline(file,s);
		std::string name = s;
		std::cout << std::endl;
		std::cout << "problem: " << name << std::endl;
		std::getline(file,s);
		n = atoi(split(s,' ')[1].c_str());
		std::cout << "n: " << n << std::endl;
		std::getline(file,s);
		int c = atoi(split(s,' ')[1].c_str());
		std::cout << "c: " << c << std::endl;
		std::getline(file,s);
		int z = atoi(split(s,' ')[1].c_str());
		std::cout << "z: " << z << std::endl;
		capacity = c;
		std::getline(file,s);
		for(int i = 0; i < n; i++){
			std::getline(file,s);
			std::vector<std::string> l = split(s,',');
			values.push_back(atoi(l[1].c_str()));
			weights.push_back(atoi(l[2].c_str()));
		}
		int result =  knapsack(capacity,values, weights);
		high_resolution_clock::time_point t2 = high_resolution_clock::now();
		auto duration = duration_cast<milliseconds>( t2 - t1 ).count();
		    
		std::cout << "time: " << duration << " ms"<< std::endl;
		std::cout <<( (result == z)? "OK" : "FAILED" )<< std::endl;
		if(result == z){
			ok++;
		}
		std::getline(file,s);
		std::getline(file,s);
	}
	std::cout << std::endl;
	std::cout << "OK: " << ok << "/" << 100 << std::endl;
}

int main (int argc, char* argv []){
	for(int i = 1; i < argc; i++){
		testFile(argv[i]);
	}
}
	
