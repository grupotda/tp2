#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <chrono>

#include "Knapsack.h"
using namespace std::chrono;

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
        std::string s;
        int capacity, n, c, z;
        std::getline(file,s);
        std::string name = s;
        std::cout << std::endl;
        std::cout << "problem: " << name << std::endl;
        std::getline(file,s);
        n = stoi(split(s,' ')[1]);
        std::cout << "n: " << n << std::endl;
        std::getline(file,s);
        c = stoi(split(s,' ')[1]);
        std::cout << "c: " << c << std::endl;
        std::getline(file,s);
        z = stoi(split(s,' ')[1]);
        std::cout << "z: " << z << std::endl;
        capacity = c;
        
        std::vector<item_t> items;
        items.reserve(n);
        //std::vector<bool> solution(n, false);
        int weight_solution = 0;
        
        std::getline(file,s);
        for(int i = 0; i < n; i++){
            std::getline(file,s);
            std::vector<std::string> l = split(s,',');
            items.emplace_back(stoi(l[1]), stoi(l[2]));
            if (stoi(l[3]) == 1) {
                //solution[i] = true;
                weight_solution += stoi(l[2]);
            }
        }

        high_resolution_clock::time_point t1 = high_resolution_clock::now();
        Knapsack knapsack(items, capacity);
        high_resolution_clock::time_point t2 = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>( t2 - t1 ).count();

        // Ya que los elementos en la mochila pueden diferir,
        // queremos que por lo menos el peso sea menor o igual!
        bool result_ok = true;
        if (z != knapsack.profit() || weight_solution < knapsack.weight()){
            result_ok = false;
        }

        std::cout << "time: " << duration << " ms"<< std::endl;
        std::cout <<( result_ok ? "OK" : "FAILED" )<< std::endl;
        if(result_ok){
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
    
