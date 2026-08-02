import os

blog = os.path.join(os.path.dirname(os.path.dirname(__file__)), "blog")
old = 'href="../index.html#contact"'
new = 'href="../../index.html#contact"'

for name in os.listdir(blog):
    path = os.path.join(blog, name, "index.html")
    if not os.path.isfile(path):
        continue
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if old in content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.replace(old, new))
        print(f"fixed: {name}")
