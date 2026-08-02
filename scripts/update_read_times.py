#!/usr/bin/env python3
"""Calculate and update accurate read times for all blog posts."""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
WPM = 200  # technical blog average


def extract_text(html):
    match = re.search(r'<article class="blog-content">(.*?)</article>', html, re.DOTALL)
    if not match:
        return ""
    text = re.sub(r"<[^>]+>", " ", match.group(1))
    return re.sub(r"\s+", " ", text).strip()


def read_time_label(word_count):
    minutes = max(1, round(word_count / WPM))
    return f"{minutes} min", minutes


def update_post(slug, read_time):
    path = os.path.join(BLOG, slug, "index.html")
    if not os.path.isfile(path):
        return False
    with open(path, encoding="utf-8") as f:
        content = f.read()
    updated = re.sub(
        r'(<div class="blog-meta-item">⏱️ )[^<]+(</div>)',
        rf"\g<1>{read_time} read\2",
        content,
        count=1,
    )
    if updated != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        return True
    return False


def update_blog_index(slug, read_time):
  pass  # handled in bulk below


def main():
    manifest = []
    for name in sorted(os.listdir(BLOG)):
        path = os.path.join(BLOG, name, "index.html")
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        words = len(extract_text(html).split())
        label, _ = read_time_label(words)
        update_post(name, label)
        manifest.append((name, words, label))
        print(f"{label:>6}  {words:4d} words  {name}")

    index_path = os.path.join(BLOG, "index.html")
    with open(index_path, encoding="utf-8") as f:
        index = f.read()

    for slug, _, label in manifest:
        pattern = rf'(<a href="{re.escape(slug)}/"[^>]*>.*?<span class="blog-card-readtime">)[^<]+(</span>)'
        index, n = re.subn(pattern, rf"\g<1>{label}\2", index, count=1, flags=re.DOTALL)
        if n == 0:
            print(f"Warning: index card not updated for {slug}")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index)

    print(f"\nUpdated {len(manifest)} posts at {WPM} WPM.")


if __name__ == "__main__":
    main()
