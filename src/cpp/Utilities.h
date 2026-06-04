#ifndef UTILITIES_H
#define UTILITIES_H

#include <cstdlib>
#include <queue>
#include <vector>

using namespace std;

inline static void clearScreen() {
#ifdef _WIN32
    std::system("cls");
#else
    std::system("clear");
#endif
}

class QueueBoardChanges {
    private:
        size_t vectorsPerBlock = 8;
        int row, column;
        queue<vector<vector<int>>> changesInBoard;
        vector<vector<vector<int>>> blocks;

        QueueBoardChanges(int row = 10, int column = 10) : row(row), column(column) {}

    public:
        QueueBoardChanges(const QueueBoardChanges&) = delete;
        QueueBoardChanges& operator = (const QueueBoardChanges&) = delete;

        static QueueBoardChanges& getInstance() {
            static QueueBoardChanges instance;
            return instance;
        }
        
        void setDimensions(int rowDimension, int columnDimension) {
            row = rowDimension;
            column = columnDimension;
        }

        void addCurrentBoard(vector<vector<int>> current) {
            changesInBoard.push(current);
        }

        void printBlocksOfFour() {
            queue<vector<vector<int>>> copy = changesInBoard; 
            cout << "\nShowing a total of " << copy.size() << " generation changes\n\n";
            
            while(!copy.empty()) {
                blocks.clear();
                while(blocks.size() < vectorsPerBlock && !copy.empty()) {
                    blocks.push_back(copy.front());
                    copy.pop();
                }

                for(int i = 0; i < row; i++) {
                    for(size_t m = 0; m < blocks.size(); m++){
                        for(int j = 0; j < column; j++) {
                            cout << blocks[m][i][j] << " ";
                        }
                        if(m < blocks.size() -1) {
                            cout << "   ";
                        }
                    }
                    cout << "\n";
                }
                cout << "\n";
            }
        }

        ~QueueBoardChanges() {};

};

#endif
