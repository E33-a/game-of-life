#ifndef GAMEBOARD_H
#define GAMEBOARD_H

#include <vector>
#include <cstdlib>
#include <ctime>
#include "Utilities.h"

using namespace std;

class GameBoard {
    private:
        int rowLimit, columnLimit;
        vector<vector<int>> grid;
        vector<vector<int>> nextGeneration;

        GameBoard() : rowLimit(0), columnLimit(0) {
            srand(time(0));
        }

    public:
        GameBoard(const GameBoard&) = delete;
        GameBoard& operator = (const GameBoard&) = delete;

        static GameBoard& getInstance() {
            static GameBoard instance;
            return instance;
        }
        
        bool isValidPosition(int targetRow, int targetColumn) {
            return (targetRow >= 0 && targetRow < rowLimit) && (targetColumn >= 0 && targetColumn < columnLimit);
        }

        void generateGridAndFill(int rows, int columns) {
            QueueBoardChanges& boardChanges = QueueBoardChanges::getInstance();
            rowLimit = rows;
            columnLimit = columns;
            grid.assign(rows, vector<int>(columns, 0));
            nextGeneration.assign(rows, vector<int>(columns, 0));

            for(int i = 0; i < rows; i++) {
                for(int j = 0; j < columns; j++) {
                    grid[i][j] = rand() % 2;
                }
            }
            boardChanges.addCurrentBoard(grid);
        }

        bool isAlive(int row, int column) {
            return grid[row][column] == 1;
        }

        int countLiveNeighbors(int row, int column) {
            int count = 0;
            for (int i = row - 1; i <= row + 1; i++) {
                for (int j = column - 1; j <= column + 1; j++) {
                    if (i == row && j == column) {
                        continue;
                    }
                    if (isValidPosition(i, j) && isAlive(i, j)) {
                        count++;
                    }
                }
            }
            return count;
        }

        void applyGameOfLifeRules() {
            QueueBoardChanges& boardChanges = QueueBoardChanges::getInstance();
            
            for(int i = 0; i < rowLimit; i++) {
                for(int j = 0; j < columnLimit; j++) {
                    int liveNeighbors = countLiveNeighbors(i, j);
                    
                    if (isAlive(i, j)) {
                        // Cell is alive
                        if (liveNeighbors == 2 || liveNeighbors == 3) {
                            nextGeneration[i][j] = 1; // Stays alive
                        } else {
                            nextGeneration[i][j] = 0; // Dies (overpopulation or underpopulation)
                        }
                    } else {
                        // Cell is dead
                        if (liveNeighbors == 3) {
                            nextGeneration[i][j] = 1; // Revives
                        } else {
                            nextGeneration[i][j] = 0; // Stays dead
                        }
                    }
                }
            }
            
            grid = nextGeneration;
            boardChanges.addCurrentBoard(grid);
        }

        bool hasLiveCells() {
            for(int i = 0; i < rowLimit; i++) {
                for(int j = 0; j < columnLimit; j++) {
                    if(grid[i][j] == 1) {
                        return true;
                    }
                }
            }
            return false;
        }

        void printGrid() {
            cout << "\nGeneration Board: \n";

            for (int i = 0; i < rowLimit; i++) {
                for (int j = 0; j < columnLimit; j++) {
                    cout << grid[i][j] << " ";
                }
                cout << endl;
            }
            cout << endl;
        }

};

#endif
