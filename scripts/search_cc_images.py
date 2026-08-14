import json
import urllib.request
import urllib.parse

topics = [
    "database evolution",
    "cache",
    "wide column database",
    "graph database",
    "monitoring dashboard",
    "vector database",
    "retrieval augmented generation",
    "database sharding",
    "database replication",
    "database partitioning",
    "database replica",
    "database cluster",
    "AWS architecture",
    "Microsoft Azure",
    "Azure AI",
    "Google Cloud",
    "OLTP OLAP",
    "AI architecture",
    "data pipeline",
    "knowledge graph",
]

def search(topic):
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": topic,
        "gsrnamespace": "6",
        "gsrlimit": "3",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "format": "json",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "brittocj.com/1.0 (blog image search)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        pages = data.get("query", {}).get("pages", {})
        results = []
        for page in pages.values():
            title = page.get("title", "")
            ii = page.get("imageinfo", [{}])[0]
            img_url = ii.get("url", "")
            ext = ii.get("extmetadata", {})
            license = ext.get("LicenseShortName", {}).get("value", "unknown")
            # Skip PDFs and non-image files
            if not title.lower().endswith((".pdf", ".ogg", ".ogv", ".webm")):
                results.append((title, img_url, license))
        return results
    except Exception as e:
        return [("ERROR", str(e), "")]

for topic in topics:
    results = search(topic)
    print(f"=== {topic} ===")
    for title, url, license in results[:3]:
        print(f"  {title} | {license} | {url}")
    print()