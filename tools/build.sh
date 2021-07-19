#!/bin/sh
set -e

IMAGES="images/lupines.webp images/skunksub.webp images/punk-skunk.webp images/skunk-octopus.jpg images/PunkSkunk-HD-TygerwolfeDesigns2019.webp"
FILES_TO_COPY="index.html saa5050.woff2 sparks-story/index.html favicon.svg"

build_image() {
    local src=$1
    local dest="build/${src%.*}"

    mkdir -p build/images
    cp "src/$src" "build/$src"
	convert -strip -scale 960x -quality 80 "src/$src" "$dest-960.webp"
    convert -strip -scale 256x -quality 60 "src/$src" "$dest-thumbnail.webp"
}

rm -r build public || true
mkdir build public

for image in $IMAGES; do
    build_image "$image" &
done
wait

for f in $FILES_TO_COPY; do
    mkdir -p "build/$(dirname "$f")"
    cp "src/$f" "build/$f"
done

tools/hasp src/css/index.hcss | tools/tidy-css.py -o build/index.css

./tools/use_hashed_assets.py build public
