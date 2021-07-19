.PHONY: build clean watch

build:
	./tools/build.sh

clean:
	-rm -r build public

watch:
	find ./src/ Makefile | entr make
