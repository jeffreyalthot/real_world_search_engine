"""Génère un squelette massif pour programme de R&D industrielle.

Usage:
    python scripts/scaffold_generator.py --root generated --files 2500 --lines-per-file 60
"""

from __future__ import annotations

import argparse
from pathlib import Path

TEMPLATE = '''"""Auto-generated scaffold file."""

class GeneratedComponent{index}:
    """Composant généré automatiquement pour structurer le programme."""

    def __init__(self) -> None:
        self.component_id = "cmp-{index:05d}"

    def describe(self) -> str:
        return "Generated component {index}"

'''


def generate(root: Path, files: int, lines_per_file: int) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for i in range(files):
        group = root / f"module_{i // 100:03d}"
        group.mkdir(parents=True, exist_ok=True)
        path = group / f"component_{i:05d}.py"
        content = TEMPLATE.format(index=i)
        extra = max(0, lines_per_file - len(content.splitlines()))
        filler = "\n".join(f"# filler line {n}" for n in range(extra))
        path.write_text(content + filler + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="generated_scaffold")
    parser.add_argument("--files", type=int, default=2500)
    parser.add_argument("--lines-per-file", type=int, default=60)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate(Path(args.root), args.files, args.lines_per_file)
    print(f"Generated {args.files} files into {args.root}")


if __name__ == "__main__":
    main()
