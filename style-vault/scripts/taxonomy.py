#!/usr/bin/env python3
"""Style Vault taxonomy query tool.

Query the taxonomy system (categories, tags, platforms, types, themes) and
see which items use each value. Helps AI agents pick valid slugs when
authoring product MDs and answer "what's in the vault" questions precisely.

USAGE
    taxonomy.py                              Overview of everything
    taxonomy.py categories                   List categories + product counts
    taxonomy.py category <slug>              Items in a category
    taxonomy.py tags                         List all tag groups + counts
    taxonomy.py tags <group>                 Values of one tag group
    taxonomy.py tag <group> <value>          Items with this tag value
    taxonomy.py platforms                    List platforms
    taxonomy.py platform <slug>              Items on a platform
    taxonomy.py types                        List entry types
    taxonomy.py type <slug>                  All items of a type
    taxonomy.py themes                       List themes
    taxonomy.py theme <slug>                 Items with a theme
    taxonomy.py item <id>                    Full details + refs of one item
    taxonomy.py search [--type] [--category] [--aesthetic] [--mood]
                       [--stack] [--platform] [--theme] [--name <substr>]
                                             Multi-filter search

FLAGS
    --json                                   Machine-readable JSON output

REQUIRES
    PyYAML  (pip install pyyaml)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("Error: PyYAML required. Install: pip install pyyaml\n")
    sys.exit(1)

SKILL_ROOT = Path(__file__).resolve().parent.parent
REFS_DIR = SKILL_ROOT / "references"
TAXONOMY_FILE = SKILL_ROOT / "assets" / "taxonomy.json"


# --- loaders ---

def load_taxonomy() -> dict:
    with TAXONOMY_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_items() -> list[dict]:
    """Parse all entry MD files under references/, return frontmatter dicts."""
    items: list[dict] = []
    for md in sorted(REFS_DIR.rglob("*.md")):
        rel = md.relative_to(REFS_DIR)
        # skip meta folders / files starting with _
        if any(seg.startswith("_") for seg in rel.parts):
            continue
        # skip top-level README
        if rel.name == "README.md" and len(rel.parts) == 1:
            continue
        text = md.read_text(encoding="utf-8")
        fm = _extract_frontmatter(text)
        if fm is None:
            continue
        fm["_path"] = str(rel)
        items.append(fm)
    return items


def _extract_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None


# --- counters ---

def _count_category(items, slug):
    return sum(1 for i in items if i.get("category") == slug)


def _count_type(items, slug):
    return sum(1 for i in items if i.get("type") == slug)


def _count_platform(items, slug):
    return sum(1 for i in items if slug in (i.get("platforms") or []))


def _count_theme(items, slug):
    return sum(1 for i in items if i.get("theme") == slug)


def _count_tag(items, group, value):
    return sum(1 for i in items if value in ((i.get("tags") or {}).get(group) or []))


# --- filtering ---

def _matches(item, filters):
    if filters.get("type") and item.get("type") != filters["type"]:
        return False
    if filters.get("category") and item.get("category") != filters["category"]:
        return False
    if filters.get("platform"):
        ps = item.get("platforms") or []
        if filters["platform"] not in ps and "any" not in ps:
            return False
    if filters.get("theme"):
        t = item.get("theme")
        if t != filters["theme"] and t != "both":
            return False
    tags = item.get("tags") or {}
    for key in ("aesthetic", "mood", "stack"):
        want = filters.get(key)
        if want and want not in (tags.get(key) or []):
            return False
    if filters.get("name"):
        if filters["name"].lower() not in (item.get("name") or "").lower():
            return False
    return True


# --- formatters ---

def _fmt_item_line(item):
    ident = item.get("id", "?")
    name = item.get("name", "")
    ty = item.get("type", "")
    return f"  {ident:<48} [{ty:<9}] {name}"


def _out_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


# --- commands ---

def cmd_overview(tax, items, as_json):
    data = {
        "total_items": len(items),
        "types": {
            slug: {"zh": meta["zh"], "count": _count_type(items, slug)}
            for slug, meta in tax["type"].items()
        },
        "categories": {
            slug: {"zh": meta["zh"], "order": meta["order"], "count": _count_category(items, slug)}
            for slug, meta in sorted(tax["category"].items(), key=lambda x: x[1]["order"])
        },
        "platforms": {
            slug: {"zh": meta["zh"], "count": _count_platform(items, slug)}
            for slug, meta in tax["platform"].items()
        },
        "themes": {
            slug: {"zh": meta["zh"], "count": _count_theme(items, slug)}
            for slug, meta in tax["theme"].items()
        },
        "tags": {
            g: {
                "groupZh": grp["groupZh"],
                "values": {
                    val: {"zh": vm["zh"], "count": _count_tag(items, g, val)}
                    for val, vm in grp["values"].items()
                },
            }
            for g, grp in tax["tag"].items()
        },
    }
    if as_json:
        _out_json(data)
        return

    print("=== Style Vault Taxonomy ===")
    print(f"Total items: {data['total_items']}\n")

    print("Types:")
    for slug, info in data["types"].items():
        print(f"  {slug:<12} {info['zh']:<6} {info['count']:>3}")

    print("\nCategories (products only):")
    for slug, info in data["categories"].items():
        print(f"  {info['order']}. {slug:<14} {info['zh']:<10} {info['count']:>3}")

    print("\nPlatforms:")
    for slug, info in data["platforms"].items():
        print(f"  {slug:<10} {info['zh']:<8} {info['count']:>3}")

    print("\nThemes:")
    for slug, info in data["themes"].items():
        print(f"  {slug:<8} {info['zh']:<8} {info['count']:>3}")

    print("\nTags:")
    for g, gi in data["tags"].items():
        print(f"  [{g}] {gi['groupZh']}")
        for val, vi in gi["values"].items():
            print(f"    {val:<22} {vi['zh']:<12} {vi['count']:>3}")
        print()


def cmd_categories(tax, items, as_json):
    cats = sorted(tax["category"].items(), key=lambda x: x[1]["order"])
    data = [
        {"slug": slug, "zh": m["zh"], "order": m["order"], "dot": m["dot"],
         "count": _count_category(items, slug)}
        for slug, m in cats
    ]
    if as_json:
        _out_json(data)
        return
    print("Categories:")
    for c in data:
        print(f"  {c['order']}. {c['slug']:<14} {c['zh']:<10} {c['count']:>3} products  {c['dot']}")


def cmd_category(slug, tax, items, as_json):
    if slug not in tax["category"]:
        sys.stderr.write(f"Error: category '{slug}' not found. Valid: {', '.join(tax['category'])}\n")
        sys.exit(1)
    m = tax["category"][slug]
    matched = [i for i in items if i.get("category") == slug]
    if as_json:
        _out_json({
            "slug": slug, "zh": m["zh"], "count": len(matched),
            "items": [{"id": i["id"], "name": i["name"]} for i in matched],
        })
        return
    print(f"Category: {slug} · {m['zh']} ({len(matched)} products)")
    for i in matched:
        print(_fmt_item_line(i))


def cmd_tags(tax, items, as_json, group):
    if group is not None:
        if group not in tax["tag"]:
            sys.stderr.write(f"Error: tag group '{group}' not found. Valid: {', '.join(tax['tag'])}\n")
            sys.exit(1)
        grp = tax["tag"][group]
        data = [
            {"slug": val, "zh": m["zh"], "count": _count_tag(items, group, val)}
            for val, m in grp["values"].items()
        ]
        if as_json:
            _out_json({"group": group, "groupZh": grp["groupZh"], "values": data})
            return
        print(f"Tag group: {group} · {grp['groupZh']}")
        for v in data:
            print(f"  {v['slug']:<22} {v['zh']:<12} {v['count']:>3}")
    else:
        out = {}
        for g, grp in tax["tag"].items():
            out[g] = {
                "groupZh": grp["groupZh"],
                "values": {
                    val: {"zh": m["zh"], "count": _count_tag(items, g, val)}
                    for val, m in grp["values"].items()
                },
            }
        if as_json:
            _out_json(out)
            return
        print("Tag groups:")
        for g, gi in out.items():
            print(f"\n  [{g}] {gi['groupZh']}")
            for val, vi in gi["values"].items():
                print(f"    {val:<22} {vi['zh']:<12} {vi['count']:>3}")


def cmd_tag(group, value, tax, items, as_json):
    if group not in tax["tag"]:
        sys.stderr.write(f"Error: tag group '{group}' not found.\n")
        sys.exit(1)
    grp = tax["tag"][group]
    if value not in grp["values"]:
        sys.stderr.write(f"Error: value '{value}' not in group '{group}'. "
                         f"Valid: {', '.join(grp['values'])}\n")
        sys.exit(1)
    zh = grp["values"][value]["zh"]
    matched = [i for i in items if value in ((i.get("tags") or {}).get(group) or [])]
    if as_json:
        _out_json({
            "group": group, "value": value, "zh": zh, "count": len(matched),
            "items": [{"id": i["id"], "type": i["type"], "name": i["name"]} for i in matched],
        })
        return
    print(f"Tag: {group}/{value} · {zh} ({len(matched)} items)")
    for i in matched:
        print(_fmt_item_line(i))


def cmd_dim_list(dim, tax, items, as_json):
    counter = {"platform": _count_platform, "type": _count_type, "theme": _count_theme}[dim]
    data = [
        {"slug": slug, "zh": m["zh"], "count": counter(items, slug),
         **{k: v for k, v in m.items() if k != "zh"}}
        for slug, m in tax[dim].items()
    ]
    if as_json:
        _out_json(data)
        return
    print(f"{dim.capitalize()}s:")
    for d in data:
        print(f"  {d['slug']:<14} {d['zh']:<10} {d['count']:>3}")


def cmd_dim_filter(dim, value, tax, items, as_json):
    if value not in tax[dim]:
        sys.stderr.write(f"Error: {dim} '{value}' not found. Valid: {', '.join(tax[dim])}\n")
        sys.exit(1)
    zh = tax[dim][value]["zh"]
    if dim == "platform":
        matched = [i for i in items if value in (i.get("platforms") or [])]
    elif dim == "type":
        matched = [i for i in items if i.get("type") == value]
    elif dim == "theme":
        matched = [i for i in items if i.get("theme") == value]
    else:
        matched = []
    if as_json:
        _out_json({
            "dimension": dim, "slug": value, "zh": zh, "count": len(matched),
            "items": [{"id": i["id"], "type": i["type"], "name": i["name"]} for i in matched],
        })
        return
    print(f"{dim.capitalize()}: {value} · {zh} ({len(matched)} items)")
    for i in matched:
        print(_fmt_item_line(i))


def cmd_item(ident, items, as_json):
    found = next((i for i in items if i.get("id") == ident), None)
    if not found:
        sys.stderr.write(f"Error: item '{ident}' not found.\n")
        sys.exit(1)
    if as_json:
        _out_json(found)
        return
    print(f"=== {found.get('name', '?')} ===")
    print(f"id:          {found.get('id')}")
    print(f"type:        {found.get('type')}")
    print(f"description: {found.get('description', '')}")
    if found.get("category"):
        print(f"category:    {found['category']}")
    if found.get("platforms"):
        print(f"platforms:   {', '.join(found['platforms'])}")
    if found.get("theme"):
        print(f"theme:       {found['theme']}")
    tags = found.get("tags") or {}
    for g in ("aesthetic", "mood", "stack"):
        if tags.get(g):
            print(f"tags.{g:<10} {', '.join(tags[g])}")
    refs = found.get("refs") or {}
    if refs:
        print("refs:")
        if refs.get("style"):
            print(f"  style:      {refs['style']}")
        for k in ("pages", "blocks", "components"):
            if refs.get(k):
                print(f"  {k}:")
                for r in refs[k]:
                    print(f"    - {r}")
        if refs.get("tokens"):
            print("  tokens:")
            for tk, tv in refs["tokens"].items():
                print(f"    {tk:<12} {tv}")


def cmd_search(filters, items, as_json):
    matched = [i for i in items if _matches(i, filters)]
    if as_json:
        _out_json({
            "filters": {k: v for k, v in filters.items() if v},
            "count": len(matched),
            "items": [{"id": i["id"], "type": i["type"], "name": i["name"]} for i in matched],
        })
        return
    active = [f"{k}={v}" for k, v in filters.items() if v]
    print(f"Search ({', '.join(active) if active else 'no filters'}): {len(matched)} matches")
    for i in matched:
        print(_fmt_item_line(i))


# --- CLI ---

def build_parser():
    # --json works both before and after the subcommand
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="Output as JSON")

    p = argparse.ArgumentParser(
        prog="taxonomy", description="Query style-vault taxonomy.",
        parents=[common],
    )
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("overview", parents=[common], help="Full taxonomy overview")

    sub.add_parser("categories", parents=[common], help="List all categories")
    pc = sub.add_parser("category", parents=[common], help="Items in a category")
    pc.add_argument("slug")

    pts = sub.add_parser("tags", parents=[common], help="List tag groups (or values of one group)")
    pts.add_argument("group", nargs="?")
    pt = sub.add_parser("tag", parents=[common], help="Items with a specific tag value")
    pt.add_argument("group")
    pt.add_argument("value")

    sub.add_parser("platforms", parents=[common], help="List platforms")
    pp = sub.add_parser("platform", parents=[common], help="Items on a platform")
    pp.add_argument("slug")

    sub.add_parser("types", parents=[common], help="List types")
    pty = sub.add_parser("type", parents=[common], help="Items of a type")
    pty.add_argument("slug")

    sub.add_parser("themes", parents=[common], help="List themes")
    pth = sub.add_parser("theme", parents=[common], help="Items with a theme")
    pth.add_argument("slug")

    pi = sub.add_parser("item", parents=[common], help="Details of one item")
    pi.add_argument("id")

    ps = sub.add_parser("search", parents=[common], help="Multi-filter search")
    ps.add_argument("--type")
    ps.add_argument("--category")
    ps.add_argument("--aesthetic")
    ps.add_argument("--mood")
    ps.add_argument("--stack")
    ps.add_argument("--platform")
    ps.add_argument("--theme")
    ps.add_argument("--name")

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    tax = load_taxonomy()
    items = load_items()
    as_json = args.json
    cmd = args.cmd or "overview"

    if cmd == "overview":
        cmd_overview(tax, items, as_json)
    elif cmd == "categories":
        cmd_categories(tax, items, as_json)
    elif cmd == "category":
        cmd_category(args.slug, tax, items, as_json)
    elif cmd == "tags":
        cmd_tags(tax, items, as_json, args.group)
    elif cmd == "tag":
        cmd_tag(args.group, args.value, tax, items, as_json)
    elif cmd == "platforms":
        cmd_dim_list("platform", tax, items, as_json)
    elif cmd == "platform":
        cmd_dim_filter("platform", args.slug, tax, items, as_json)
    elif cmd == "types":
        cmd_dim_list("type", tax, items, as_json)
    elif cmd == "type":
        cmd_dim_filter("type", args.slug, tax, items, as_json)
    elif cmd == "themes":
        cmd_dim_list("theme", tax, items, as_json)
    elif cmd == "theme":
        cmd_dim_filter("theme", args.slug, tax, items, as_json)
    elif cmd == "item":
        cmd_item(args.id, items, as_json)
    elif cmd == "search":
        filters = {
            k: getattr(args, k)
            for k in ("type", "category", "aesthetic", "mood", "stack",
                      "platform", "theme", "name")
        }
        cmd_search(filters, items, as_json)


if __name__ == "__main__":
    main()
