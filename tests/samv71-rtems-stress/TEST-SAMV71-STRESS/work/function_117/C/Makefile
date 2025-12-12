VISUAL?=kate

all: compile-linux

clean:
	rm -rf obj

edit:
	$(VISUAL) ../../dataview/C/dataview-uniq.h \
                  src/function_117.h \
                  src/function_117.c

compile-linux:
	mkdir -p obj && cd obj && gcc -c ../src/*.c
