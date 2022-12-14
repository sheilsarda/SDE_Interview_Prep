CFLAGS=-g -Wall
CC=g++
SRCS= main.cpp GarageDoor.cpp
OBJS1= main.o  GarageDoor.o
OBJS2= GarageDoor.o 
LDFLAGS=
LIBS= -pthread

all:  garageDoor
test: garageDoor

$(SRCS):
	$(CC) $(CFLAGS) -c $*.c

garageDoor: $(SHELL_OBJ) $(OBJS1)
	$(CC) $(LDFLAGS) $(LIBS) -o garageDoor $(SHELL_OBJ) $(OBJS1)
test: $(SHELL_OBJ) $(OBJS2)
	$(CC) $(LDFLAGS) $(LIBS) -o garageDoor $(SHELL_OBJ) $(OBJS2)
clean:
	rm -f *.o garageDoor