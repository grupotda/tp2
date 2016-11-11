#pragma once

#include <vector>

typedef struct item
{
    int value;
    int weight;
    item(int v, int w): value(v), weight(w) {}
} item_t;

class Knapsack
{
private:
    int m_profit; // ganancia optima
    int m_weight; // peso asociado a la ganancia optima
    std::vector<bool> m_kept; // del tamaño de items, indica si esta o no.
public:
    Knapsack(const std::vector<item_t>& items, int capacity);
    ~Knapsack();
    // Devuelve la ganancia optima.
    int profit() {return m_profit;};
    // Devuelve el peso asociado a la ganancia optima.
    int weight() {return m_weight;};
    // Devuelve un arreglo del tamaño de items que indica si en esa posicion
    // el elemento de items esta en la solucion optima.
    const std::vector<bool>& solution() {return m_kept;};
};

