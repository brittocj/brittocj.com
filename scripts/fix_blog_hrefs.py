import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent

index = root / "index.html"
text = index.read_text(encoding="utf-8")
text = text.replace('href="blog/"', 'href="blog/index.html"')
index.write_text(text, encoding="utf-8")

blog_index = root / "blog" / "index.html"
text = blog_index.read_text(encoding="utf-8")
text = text.replace('href="./" class="active">Blog', 'href="index.html" class="active">Blog')
text = re.sub(
    r'href="([a-z0-9-]+)/" class="blog-card"',
    r'href="\1/index.html" class="blog-card"',
    text,
)
blog_index.write_text(text, encoding="utf-8")

for post in (root / "blog").glob("*/index.html"):
    text = post.read_text(encoding="utf-8")
    new = text.replace('href="../">Blog', 'href="../index.html">Blog')
    new = new.replace(
        'href="../">← Back to All Posts',
        'href="../index.html">← Back to All Posts',
    )
    if new != text:
        post.write_text(new, encoding="utf-8")
        print(f"updated {post.relative_to(root)}")

print("done")
