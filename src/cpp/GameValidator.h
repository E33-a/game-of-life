#ifndef GAMEVALIDATOR_H
#define GAMEVALIDATOR_H

#include "Utilities.h"
#include <iostream>

using namespace std;

class GameValidator {
private:
  int rowIndex, columnIndex;

public:
  GameValidator() : rowIndex(0), columnIndex(0) {}

  int getRowIndex() { return rowIndex; }

  int getColumnIndex() { return columnIndex; }

  void getData() {
    do {
      cout << "Enter the rows (10 or more):    ";
      cin >> rowIndex;
      if (rowIndex < 10 || rowIndex > 100) {
        cout << "Invalid value. Try again.\n";
        if (rowIndex > 100)
          cout << "Please enter fewer rows; very large values may use a lot of memory.\n\n";
      }
    } while (rowIndex < 10 || rowIndex > 100);

    do {
      cout << "Enter the columns (10 or more):     ";
      cin >> columnIndex;
      if (columnIndex < 10 || columnIndex > 100) {
        cout << "Invalid value. Try again.\n\n";
        if (columnIndex > 100)
          cout << "Please enter fewer columns; very large values may use a lot of memory.\n";
      }
    } while (columnIndex < 10 || columnIndex > 100);
    clearScreen();
  }

  ~GameValidator() {}
};

#endif
