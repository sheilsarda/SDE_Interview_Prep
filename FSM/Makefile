CFLAGS=-g -Wall
CC=g++
SRCS= main.cpp
OBJS= main.o
LDFLAGS=-std=c++17
LIBS=

all:    garageDoor

$(SRCS):
	$(CC) $(CFLAGS) -c $*.c

garageDoor: $(SHELL_OBJ) $(OBJS)
	$(CC) $(LDFLAGS) $(LIBS) -o garageDoor $(SHELL_OBJ) $(OBJS)

clean:
	rm -f *.o garageDoor