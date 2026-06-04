CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
TARGET = game_of_life.exe
SOURCES = main.cpp
HEADERS = GameBoard.h GameSimulator.h GameValidator.h Utilities.h
OBJECTS = $(SOURCES:.cpp=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

%.o: %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS) $(TARGET)

.PHONY: all clean
