#ifndef GAMESIMULATOR_H
#define GAMESIMULATOR_H

#include <iostream>
#include "GameBoard.h"

using namespace std;

class GameSimulator {
public:
    void startSimulation() {
        GameBoard& board = GameBoard::getInstance();
        char option;
        int generationCount = 0;

        do {
            generationCount++;
            cout << "Generation: " << generationCount << " \n";
            
            board.printGrid();

            board.applyGameOfLifeRules();

            cout << "After applying Game of Life rules: \n";
            board.printGrid();

            if (!board.hasLiveCells()) {
                cout << "All cells are dead. Simulation ended.";
                break;
            }

            cout << "Continue simulation? (y/n): ";
            cin >> option;

        } while (option == 'y' || option == 'Y');

        cout << "\nSimulation finished at generation: " << generationCount;
    }
};

#endif
