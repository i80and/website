#!/usr/bin/env python3
import hashlib
import os
from pathlib import Path, PurePosixPath
from typing import Match, Dict
import re
import sys
import shutil

PAT_HREF_CSS = re.compile(r"href=\"([^\"]*\.css)\"")
PAT_IMAGES = re.compile(r"src(?:set)?=\"([^\"]*)\"")
PAT_CSS_URL = re.compile(r"url\(\"?([^\"\)]+)\"?\)")


def process_asset(path: Path) -> Path:
    hasher = hashlib.sha512(path.read_bytes())
    sha512 = hasher.hexdigest()[:16]
    return path.with_name(f"immut-{path.stem}-{sha512}{path.suffix}")


def main() -> None:
    assets: Dict[Path, Path] = {}
    root = Path(sys.argv[1])
    output_root = Path(sys.argv[2])
    shutil.rmtree(output_root, ignore_errors=True)
    for path in root.glob("**/*"):
        if not path.is_file():
            continue
        dest_path = output_root.joinpath(Path(*path.parts[len(root.parts) :]))
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix in {".html", ".css"}:
            data = path.read_text()

            def replace(match: Match) -> str:
                match_path = path.parent.joinpath(Path(match.group(1)))
                new_match_path = process_asset(match_path)
                assets[
                    match_path.resolve().relative_to(root.resolve())
                ] = new_match_path.resolve().relative_to(root.resolve())
                updated_path = PurePosixPath(match.group(1))
                updated_path = updated_path.with_name(
                    new_match_path.stem + updated_path.suffix
                )
                return match.group(0).replace(match.group(1), updated_path.as_posix())

            if path.suffix == ".html":
                data = PAT_HREF_CSS.sub(replace, data)
                data = PAT_IMAGES.sub(replace, data)
            elif path.suffix == ".css":
                data = PAT_CSS_URL.sub(replace, data)

            dest_path.write_text(data)
        else:
            shutil.copy2(path, dest_path)

    for orig_asset_path, new_asset_path in assets.items():
        output_root.joinpath(orig_asset_path).replace(
            output_root.joinpath(new_asset_path)
        )


if __name__ == "__main__":
    main()
