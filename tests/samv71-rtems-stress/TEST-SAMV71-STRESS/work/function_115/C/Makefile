VISUAL?=kate

all: compile-linux

clean:
	rm -rf obj

edit:
	$(VISUAL) ../../dataview/C/dataview-uniq.h \
                  src/function_115.h \
                  src/function_115.c

compile-linux:
	mkdir -p obj && cd obj && gcc -c ../src/*.c
