CFLAGS=-g -Wall
CC=g++
SRCS= main.cpp DPSoln.cpp 
OBJS1= main.o  DPSoln.o
OBJS2= DPSoln.o 
LDFLAGS=
LIBS= -pthread

all:  DPSoln

$(SRCS):
	$(CC) $(CFLAGS) -c $*.c

DPSoln: $(SHELL_OBJ) $(OBJS1)
	$(CC) $(LDFLAGS) $(LIBS) -o DPSoln $(SHELL_OBJ) $(OBJS1)

clean:
	rm -f *.o DPSoln


