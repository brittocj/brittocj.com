#!/usr/bin/env python3
"""
Replace PNG image references with corresponding WebP image references
across all blog HTML files.

Skips favicon.png since no favicon.webp counterpart exists.
"""

from pathlib import Path

BLOG_DIR = Path("blog")

# Mapping of PNG filename (URL-encoded as it appears in HTML) to WebP filename (URL-encoded)
PNG_TO_WEBP = {
    "From%20SQL%20to%20Vector%20Databases.png": "From-SQL-to-Vector-Databases.webp",
    "SQL%20Databases%20%E2%80%93%20The%20Traditional%20Foundation%20image.png": "SQL-Databases-%E2%80%93-The-Traditional-Foundation-image.webp",
    "NoSQL%20When%20Tables%20Aren%27t%20Enough%20image.png": "NoSQL-When-Tables-Arent-Enough-image.webp",
    "Key-Value%20Databases%20image.png": "Key-Value-Databases-image.webp",
    "Database%20Caching%20image.png": "Database-Caching-image.webp",
    "Wide-Column%20Databases%20image.png": "Wide-Column%20Databases%20image.webp",
    "Graph%20Databases%20image.png": "Graph-Databases-image.webp",
    "Time-Series%20Databases%20image.png": "Time-Series-Databases-image.webp",
    "Vector%20Databases%20The%20AI%20Era%20image.png": "Vector-Databases-The-AI-Era-image.webp",
    "The%20Rise%20of%20Multi-Model%20Databases%20image.png": "The-Rise-of-Multi-Model-Databases-image.webp",
    "Database%20Sharding%20image.png": "Database-Sharding-image.webp",
    "Database%20Replication%20image.png": "Database-Replication-image.webp",
    "Database%20Partitioning.png": "Database-Partitioning.webp",
    "Read%20Replicas%20image.png": "Read-Replicas-image.webp",
    "Database%20Clustering%20image.png": "Database-Clustering-image.webp",
    "Managed%20Databases%20on%20Public%20Cloud%20image.png": "Managed-Databases-on-Public-Cloud-image.webp",
    "Typical%20AWS%20Architecture%20image.png": "Typical-AWS-Architecture-image.webp",
    "Typical%20Azure%20Architecture.png": "Typical-Azure-Architecture.webp",
    "Typical%20Google%20Cloud%20Architecture.png": "Typical-Google-Cloud-Architecture.webp",
    "Modern%20Database%20Architecture%20image.png": "Modern-Database-Architecture-image.webp",
    "The%20Future%20Database%20%2B%20AI.png": "The-Future-Database-AI.webp",
    "mahabharata-human-body.png": "mahabharata-human-body.webp",
    "agentic-ai-banner.png": "agentic-ai-banner.webp",
    "aws-eks-microservices.png": "aws-eks-microservices.webp",
    "azure-aks-microservices.png": "azure-aks-microservices.webp",
    "gcp-gke-microservices.png": "gcp-gke-microservices.webp",
    "oci-oke-microservices.png": "oci-oke-microservices.webp",
    "google-us-order-confirmation.png": "google-us-order-confirmation.webp",
}


def main() -> None:
    total_replacements = 0
    for html_file in sorted(BLOG_DIR.rglob("*.html")):
        original = html_file.read_text(encoding="utf-8")
        updated = original
        for png_name, webp_name in PNG_TO_WEBP.items():
            count = updated.count(png_name)
            if count:
                updated = updated.replace(png_name, webp_name)
                total_replacements += count
                print(f"  {html_file}: {count}x {png_name} -> {webp_name}")
        if updated != original:
            html_file.write_text(updated, encoding="utf-8")
            print(f"Updated {html_file}")

    print(f"\nTotal replacements: {total_replacements}")


if __name__ == "__main__":
    main()