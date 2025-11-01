.PHONY: all environment

all: environment
	$(MAKE) -C tests

environment:
	python3 -mvenv env
	./env/bin/pip install -r requirements.txt
