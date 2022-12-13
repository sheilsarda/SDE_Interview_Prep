CFLAGS=-g -Wall
CC=g++
SRCS= main.cpp GarageDoor.cpp
OBJS= main.o  GarageDoor.o
LDFLAGS=
LIBS= -pthread

all:    garageDoor

$(SRCS):
	$(CC) $(CFLAGS) -c $*.c

garageDoor: $(SHELL_OBJ) $(OBJS)
	$(CC) $(LDFLAGS) $(LIBS) -o garageDoor $(SHELL_OBJ) $(OBJS)

clean:
	rm -f *.o garageDoor