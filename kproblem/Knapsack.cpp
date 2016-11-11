#include <cstddef>
#include "Knapsack.h"

Knapsack::Knapsack(const std::vector<item_t>& items, int capacity):
    m_kept(std::vector<bool>(items.size(), false))
{
    // Solo un arreglo de ganancia por peso, iteramos al reves para saber valores anteriores
    std::vector<int> profit(capacity + 1, 0);
    // vector<bool> es un "dynamic bitset" eficiente en espacio, para saber si esta o no el item
    std::vector<std::vector<bool>> keep(items.size(), std::vector<bool>(capacity + 1, false));
    
    for (size_t i = 0; i < items.size(); ++i) {
        const int weight = items[i].weight;
        const int value = items[i].value;

        for (int j = capacity; j >= weight; --j) {
            const int new_profit = profit[j - weight] + value;

            if (new_profit > profit[j]) {
                profit[j] = new_profit;
                keep[i][j] = true;
            }
        }
    }
    
    //Calculamos el menor peso posible que tiene la ganancia optima
    int j = capacity;
    while (profit[j] == profit[j-1]) --j;

    m_weight = j;
    m_profit = profit[m_weight];

    //Identificamos los elementos en la mochila
    for (size_t i = items.size(); i --> 0;) { // i>0;) { i--; ... }
        if (keep[i][j]) {
            j -= items[i].weight;
            m_kept[i] = true;
        }
    }
}

Knapsack::~Knapsack() {}
