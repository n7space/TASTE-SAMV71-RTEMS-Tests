VISUAL?=kate

all: compile-linux

clean:
	rm -rf obj

edit:
	$(VISUAL) ../../dataview/C/dataview-uniq.h \
                  src/function_91.h \
                  src/function_91.c

compile-linux:
	mkdir -p obj && cd obj && gcc -c ../src/*.c
