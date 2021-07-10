.PHONY: all clean watch

copy_files=index.html saa5050.woff2 sparks-story/index.html
copied_files=$(patsubst %,build/%,$(copy_files))

images=images/lupines.png
built_images_jpg=$(patsubst %.png,build/%.jpg,$(images))
built_images_webp=$(patsubst %.png,build/%.webp,$(images))


public/index.html: build/index.css $(copied_files) $(built_images_jpg) $(built_images_webp)
	./tools/use_hashed_assets.py build public

build/index.css: src/css/*
	@mkdir -p `dirname "$@"`
	tools/hasp src/css/index.hcss > $@

build/%: src/%
	@mkdir -p `dirname "$@"`
	cp $< $@

build/images/%.webp: src/images/%.png
	@mkdir -p `dirname "$@"`
	convert -quality 80 $^ $@

build/images/%.jpg: src/images/%.png
	@mkdir -p `dirname "$@"`
	convert -quality 90 $^ $@

clean:
	-rm -r build public

watch:
	find ./src/ Makefile | entr make
