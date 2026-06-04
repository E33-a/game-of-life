#include <iostream>
#include "GameBoard.h"
#include "GameValidator.h"
#include "GameSimulator.h"

using namespace std;

int main() {
    clearScreen();
    cout << "Conway's Game of Life\n\n";
    GameValidator validator;
    validator.getData();
    int rows = validator.getRowIndex();
    int columns = validator.getColumnIndex();
    
    QueueBoardChanges& queueBoardChanges = QueueBoardChanges::getInstance();
    queueBoardChanges.setDimensions(rows, columns);                                                                                              

    GameBoard& board = GameBoard::getInstance();
    board.generateGridAndFill(rows, columns);

    GameSimulator simulator;
    simulator.startSimulation();

    clearScreen();
    queueBoardChanges.printBlocksOfFour();

    cout << "\nPress ENTER to exit program...";
    cin.clear();
    cin.ignore(10000, '\n');
    cin.get();
}