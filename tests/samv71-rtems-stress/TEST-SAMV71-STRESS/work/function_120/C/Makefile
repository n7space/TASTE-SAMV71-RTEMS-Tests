VISUAL?=kate

all: compile-linux

clean:
	rm -rf obj

edit:
	$(VISUAL) ../../dataview/C/dataview-uniq.h \
                  src/function_120.h \
                  src/function_120.c

compile-linux:
	mkdir -p obj && cd obj && gcc -c ../src/*.c
