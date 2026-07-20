from __future__ import annotations

from pathlib import Path
import json

from common import build_inventory_document, find_repo_root

def main() -> int:
    root = find_repo_root()
    output = build_inventory_document(root)

    out_path = root / ".claude/control-plane/inventory.json"
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"Files inventoried: {len(output['files'])}")
    print(f"Duplicate frontmatter names: {len(output['duplicate_frontmatter_names'])}")
    return 1 if output["duplicate_frontmatter_names"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
