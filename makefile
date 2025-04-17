# Compiler and flags
CC      = gcc
CFLAGS  = -Wall -std=c11 -g -fPIC
LDFLAGS = -L.

# Directory paths
INC = include/
SRC = src/
OBJ = obj/
BIN = bin/

# Create necessary directories if they don't exist.
$(shell mkdir -p $(OBJ) $(BIN))

# Default target: build the shared library
all: $(BIN)libvcparser.so
	cp $(BIN)libvcparser.so $(BIN)main

# Build shared library
$(BIN)libvcparser.so: $(OBJ)VCParser.o $(OBJ)LinkedListAPI.o $(OBJ)VCHelpers.o
	$(CC) -shared -o $(BIN)libvcparser.so $(OBJ)VCParser.o $(OBJ)LinkedListAPI.o $(OBJ)VCHelpers.o

# Compile main.o separately (if needed for testing)
$(OBJ)main.o: $(SRC)main.c $(INC)VCParser.h $(INC)LinkedListAPI.h $(INC)VCHelpers.h
	$(CC) $(CFLAGS) -I$(INC) -c $(SRC)main.c -o $(OBJ)main.o

# Compile VCParser.o
$(OBJ)VCParser.o: $(SRC)VCParser.c $(INC)VCParser.h $(INC)LinkedListAPI.h $(INC)VCHelpers.h
	$(CC) $(CFLAGS) -I$(INC) -c $(SRC)VCParser.c -o $(OBJ)VCParser.o

# Compile LinkedListAPI.o
$(OBJ)LinkedListAPI.o: $(SRC)LinkedListAPI.c $(INC)LinkedListAPI.h $(INC)VCHelpers.h
	$(CC) $(CFLAGS) -I$(INC) -c $(SRC)LinkedListAPI.c -o $(OBJ)LinkedListAPI.o

# Compile VCHelpers.o
$(OBJ)VCHelpers.o: $(SRC)VCHelpers.c $(INC)VCHelpers.h $(INC)LinkedListAPI.h $(INC)VCParser.h
	$(CC) $(CFLAGS) -I$(INC) -c $(SRC)VCHelpers.c -o $(OBJ)VCHelpers.o

# Clean target: removes all object files and shared library files.
clean:
	rm -rf $(OBJ)*.o $(BIN)*.so $(BIN)main libvcparser.so
