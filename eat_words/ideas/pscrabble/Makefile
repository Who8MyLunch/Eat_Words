OBJ= board.o play.o cmove.o score.o util.o dict.o dat.o
CC= gcc
CFLAGS= -I/usr/pgrad/gary/src/Python-1.2/Include -g -DNDEBUG -O
#LD= ld -shared		# OSF
LD= ld -G		# solaris2

LIBS= /usr/pgrad/gary/src/python/Modules/libModules.a\
	/usr/pgrad/gary/src/python/Python/libPython.a\
	/usr/pgrad/gary/src/python/Objects/libObjects.a

all:	scrabble scrabblemodule.so

scrabblemodule.so: $(OBJ) scrabblemodule.o
	$(LD) -o scrabblemodule.so $(OBJ) scrabblemodule.o
scrabble: $(OBJ) main.o 
	$(CC) -o scrabble $(OBJ)  main.o 

$(OBJ) main.o scrabblemodule.o:	scrabble.h types.h fns.h dat.h

clean:
	rm *.o *.pyc

nuke:	clean
	rm scrabble *.so

update:	scrabblemodule.so
	cp -r *.py scrabblemodule.so bitmap $(HOME)/scrabble
	ci -l *.py *.[ch] Makefile
