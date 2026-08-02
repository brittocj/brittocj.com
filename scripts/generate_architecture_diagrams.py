#!/usr/bin/env python3
"""Generate professional microservices-on-Kubernetes architecture SVG diagrams."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "blog"

DIAGRAMS = {
    "azure-aks-architecture": {
        "title": "Microservices architecture on Azure Kubernetes Service",
        "brand": "Microsoft Azure",
        "brand_color": "#0078d4",
        "accent": "#0078d4",
        "lb": "Azure Load Balancer",
        "cluster": "Azure Kubernetes Service",
        "cni": "Azure CNI powered by Cilium",
        "pipeline": "Azure Pipelines",
        "registry": "Azure Container Registry",
        "data_stores": [
            "Azure DocumentDB",
            "Azure Cosmos DB",
            "Azure Managed Redis",
            "Azure Service Bus",
        ],
        "security": [
            ("Microsoft Entra ID", "Role-based access control"),
            ("Managed identities", ""),
            ("Azure Key Vault", ""),
            ("Log Analytics workspace", ""),
            ("Application Insights", ""),
            ("Azure Monitor", ""),
        ],
        "network_label": "Virtual network",
    },
    "aws-eks-architecture": {
        "title": "Microservices architecture on Amazon Elastic Kubernetes Service",
        "brand": "Amazon Web Services",
        "brand_color": "#232f3e",
        "accent": "#ff9900",
        "lb": "Application Load Balancer",
        "cluster": "Amazon Elastic Kubernetes Service",
        "cni": "Amazon VPC CNI",
        "pipeline": "AWS CodePipeline",
        "registry": "Amazon ECR",
        "data_stores": [
            "Amazon RDS",
            "Amazon DynamoDB",
            "Amazon ElastiCache",
            "Amazon SQS",
        ],
        "security": [
            ("AWS IAM", "Role-based access control"),
            ("IRSA", "Managed identities"),
            ("AWS Secrets Manager", ""),
            ("Amazon CloudWatch", ""),
            ("AWS X-Ray", ""),
            ("Amazon VPC", ""),
        ],
        "network_label": "Virtual network",
    },
    "gcp-gke-architecture": {
        "title": "Microservices architecture on Google Kubernetes Engine",
        "brand": "Google Cloud",
        "brand_color": "#4285f4",
        "accent": "#4285f4",
        "lb": "Cloud Load Balancing",
        "cluster": "Google Kubernetes Engine",
        "cni": "VPC-native Pod networking",
        "pipeline": "Cloud Build",
        "registry": "Artifact Registry",
        "data_stores": [
            "Cloud SQL",
            "Cloud Firestore",
            "Memorystore for Redis",
            "Pub/Sub",
        ],
        "security": [
            ("Cloud IAM", "Role-based access control"),
            ("Workload Identity", "Managed identities"),
            ("Secret Manager", ""),
            ("Cloud Logging", ""),
            ("Cloud Trace", ""),
            ("VPC Network", ""),
        ],
        "network_label": "Virtual network",
    },
    "oci-oke-architecture": {
        "title": "Microservices architecture on Oracle Kubernetes Engine",
        "brand": "Oracle Cloud",
        "brand_color": "#c74634",
        "accent": "#c74634",
        "lb": "OCI Load Balancer",
        "cluster": "Oracle Kubernetes Engine",
        "cni": "OCI VCN-Native Pod Networking",
        "pipeline": "OCI DevOps",
        "registry": "Oracle Container Registry",
        "data_stores": [
            "Autonomous Database",
            "Oracle NoSQL Database",
            "OCI Cache with Redis",
            "OCI Streaming",
        ],
        "security": [
            ("OCI IAM", "Role-based access control"),
            ("Managed identities", ""),
            ("OCI Vault", ""),
            ("OCI Logging", ""),
            ("OCI APM", ""),
            ("Virtual Cloud Network", ""),
        ],
        "network_label": "Virtual network",
    },
}


def svg_header():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 650" role="img">
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 Z" fill="#505050"/>
    </marker>
    <linearGradient id="cube" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4a90d9"/>
      <stop offset="100%" stop-color="#2b6cb0"/>
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-opacity="0.12"/>
    </filter>
  </defs>
  <rect width="1100" height="650" fill="#ffffff"/>
'''


def browser_icon(x, y):
    return f'''
  <g transform="translate({x},{y})">
    <rect x="0" y="8" width="52" height="38" rx="3" fill="#e8f4fd" stroke="#0078d4" stroke-width="1.2"/>
    <rect x="0" y="8" width="52" height="10" fill="#0078d4" rx="3"/>
    <circle cx="8" cy="13" r="2" fill="#fff"/><circle cx="14" cy="13" r="2" fill="#fff"/><circle cx="20" cy="13" r="2" fill="#fff"/>
    <rect x="8" y="24" width="36" height="3" fill="#94a3b8"/><rect x="8" y="31" width="28" height="3" fill="#cbd5e1"/>
    <text x="26" y="58" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#1e293b">Client apps</text>
  </g>'''


def lb_box(x, y, label, accent):
    return f'''
  <g transform="translate({x},{y})">
    <rect x="0" y="0" width="130" height="64" rx="4" fill="#f8fafc" stroke="{accent}" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="10" y="10" width="28" height="28" rx="14" fill="{accent}" opacity="0.15"/>
    <circle cx="24" cy="24" r="10" fill="{accent}" opacity="0.35"/>
    <text x="46" y="26" font-family="Segoe UI,Arial,sans-serif" font-size="9.5" font-weight="600" fill="#1e293b">{label}</text>
    <text x="46" y="42" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#64748b">Public IP address</text>
  </g>'''


def nginx_ingress(x, y):
    return f'''
  <g transform="translate({x},{y})">
    <rect x="0" y="0" width="110" height="58" rx="4" fill="#fff" stroke="#009639" stroke-width="1.5"/>
    <polygon points="20,12 36,12 36,46 20,46" fill="#009639"/>
    <text x="48" y="24" font-family="Segoe UI,Arial,sans-serif" font-size="10" font-weight="700" fill="#009639">NGINX</text>
    <text x="48" y="38" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#1e293b">Ingress</text>
  </g>'''


def microservice_cube(x, y, name):
    return f'''
  <g transform="translate({x},{y})">
    <polygon points="8,4 44,4 52,12 16,12" fill="#6baee8"/>
    <polygon points="8,4 16,12 16,40 8,32" fill="#3b82c4"/>
    <polygon points="44,4 52,12 52,40 44,32" fill="#2f6fad"/>
    <rect x="16" y="12" width="28" height="28" fill="url(#cube)"/>
    <text x="30" y="30" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="8" font-weight="600" fill="#fff">{name}</text>
  </g>'''


def data_store(x, y, label, accent):
    short = label if len(label) <= 24 else label[:22] + "..."
    return f'''
  <g transform="translate({x},{y})">
    <rect x="0" y="0" width="210" height="42" rx="4" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.2" filter="url(#shadow)"/>
    <rect x="10" y="11" width="20" height="20" rx="3" fill="#22c55e" opacity="0.2"/>
    <text x="38" y="26" font-family="Segoe UI,Arial,sans-serif" font-size="10.5" font-weight="600" fill="#1e293b">{short}</text>
  </g>'''


def service_box(x, y, w, h, label, color="#64748b", fill="#f8fafc"):
    lines = []
    if len(label) > 20:
        parts = label.split(" ")
        line1, line2 = "", ""
        for word in parts:
            if len(line1 + word) < 18:
                line1 = (line1 + " " + word).strip()
            else:
                line2 = (line2 + " " + word).strip()
        text = f'<text x="{w/2}" y="{h/2 - 2}" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="9" font-weight="600" fill="#1e293b">{line1}</text>'
        if line2:
            text += f'<text x="{w/2}" y="{h/2 + 10}" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="9" font-weight="600" fill="#1e293b">{line2}</text>'
    else:
        text = f'<text x="{w/2}" y="{h/2 + 4}" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="9.5" font-weight="600" fill="#1e293b">{label}</text>'
    return f'''
  <g transform="translate({x},{y})">
    <rect x="0" y="0" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{color}" stroke-width="1.2" filter="url(#shadow)"/>
    {text}
  </g>'''


def generate(cfg):
    accent = cfg["accent"]
    parts = [svg_header()]

    parts.append(f'''
  <text x="550" y="36" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="20" font-weight="700" fill="#1e293b">{cfg["title"]}</text>
  <text x="28" y="628" font-family="Segoe UI,Arial,sans-serif" font-size="11" font-weight="700" fill="{cfg["brand_color"]}">{cfg["brand"]}</text>
''')

    parts.append(browser_icon(40, 210))
    parts.append(lb_box(130, 205, cfg["lb"], accent))
    parts.append(f'<line x1="92" y1="238" x2="130" y2="238" stroke="#505050" stroke-width="1.5" marker-end="url(#arrow)"/>')

    parts.append(f'''
  <rect x="290" y="70" width="430" height="330" rx="6" fill="none" stroke="{accent}" stroke-width="2" stroke-dasharray="9,5"/>
  <text x="300" y="62" font-family="Segoe UI,Arial,sans-serif" font-size="12" font-weight="700" fill="{accent}">{cfg["cluster"]}</text>
  <rect x="305" y="85" width="400" height="280" rx="4" fill="#fafbfc" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="318" y="104" font-family="Segoe UI,Arial,sans-serif" font-size="10" font-weight="600" fill="#64748b">Kubernetes cluster</text>
''')

    parts.append('''
  <rect x="318" y="115" width="155" height="105" rx="4" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="328" y="132" font-family="Segoe UI,Arial,sans-serif" font-size="10" font-weight="600" fill="#475569">Front end Namespace</text>
''')
    parts.append(nginx_ingress(340, 140))
    parts.append(f'<line x1="250" y1="238" x2="340" y2="170" stroke="#505050" stroke-width="1.5" marker-end="url(#arrow)"/>')

    parts.append('''
  <rect x="488" y="115" width="200" height="250" rx="4" fill="#f1f5f9" stroke="#94a3b8"/>
  <text x="498" y="132" font-family="Segoe UI,Arial,sans-serif" font-size="10" font-weight="600" fill="#475569">Back end Namespace</text>
''')
    parts.append(microservice_cube(520, 145, "micro-1"))
    parts.append(microservice_cube(600, 145, "micro-2"))
    parts.append(microservice_cube(520, 200, "micro-3"))
    parts.append(microservice_cube(600, 200, "micro-4"))
    parts.append(microservice_cube(560, 255, "micro-5"))
    parts.append('''
  <line x1="473" y1="170" x2="520" y2="160" stroke="#505050" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="568" y1="160" x2="600" y2="160" stroke="#505050" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="632" y1="175" x2="548" y2="205" stroke="#505050" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="632" y1="175" x2="628" y2="205" stroke="#505050" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="632" y1="175" x2="580" y2="260" stroke="#505050" stroke-width="1.5" marker-end="url(#arrow)"/>
''')

    parts.append(f'''
  <rect x="380" y="340" width="240" height="34" rx="4" fill="#fff7ed" stroke="#f59e0b" stroke-width="1.2"/>
  <text x="500" y="361" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="10" font-weight="600" fill="#92400e">{cfg["cni"]}</text>
''')

    parts.append(f'''
  <text x="760" y="100" font-family="Segoe UI,Arial,sans-serif" font-size="11" font-weight="700" fill="#475569">External data stores</text>
''')
    for i, store in enumerate(cfg["data_stores"]):
        parts.append(data_store(745, 115 + i * 52, store, accent))
        parts.append(f'<line x1="688" y1="240" x2="745" y2="{136 + i * 52}" stroke="#505050" stroke-width="1.2" marker-end="url(#arrow)"/>')

    parts.append('''
  <rect x="40" y="440" width="150" height="70" rx="4" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.2" stroke-dasharray="6,4"/>
  <text x="52" y="458" font-family="Segoe UI,Arial,sans-serif" font-size="10" font-weight="700" fill="#6d28d9">DevOps</text>
''')
    parts.append(service_box(55, 468, 120, 34, cfg["pipeline"], "#8b5cf6", "#ede9fe"))
    parts.append(service_box(210, 468, 130, 34, cfg["registry"], "#8b5cf6", "#ede9fe"))
    parts.append(f'''
  <line x1="175" y1="485" x2="210" y2="485" stroke="#505050" stroke-width="1.2" marker-end="url(#arrow)"/>
  <line x1="115" y1="468" x2="400" y2="380" stroke="#505050" stroke-width="1.2" marker-end="url(#arrow)" stroke-dasharray="5,4"/>
  <text x="230" y="455" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#64748b">Image push</text>
  <line x1="340" y1="502" x2="390" y2="390" stroke="#505050" stroke-width="1.2" marker-end="url(#arrow)" stroke-dasharray="5,4"/>
  <text x="330" y="448" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#64748b">Image pull</text>
  <text x="250" y="430" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#64748b">Helm</text>
''')

    sec = cfg["security"]
    x_start = 40
    for i, (name, sub) in enumerate(sec):
        x = x_start + i * 155
        parts.append(service_box(x, 545, 140, 44, name))
        if sub and i == 0:
            parts.append(f'<line x1="505" y1="400" x2="{x + 70}" y2="545" stroke="#505050" stroke-width="1.2" marker-end="url(#arrow)"/>')
            parts.append(f'<text x="520" y="480" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#64748b">{sub}</text>')
        if sub and i == 1:
            parts.append(f'<line x1="{x + 70}" y1="545" x2="{x + 225}" y2="545" stroke="#505050" stroke-width="1.2" marker-end="url(#arrow)"/>')
            parts.append(f'<text x="{x + 100}" y="538" font-family="Segoe UI,Arial,sans-serif" font-size="8" fill="#64748b">{sub}</text>')

    parts.append(f'''
  <text x="900" y="590" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#64748b">{cfg["network_label"]}</text>
  <rect x="860" y="548" width="200" height="44" rx="4" fill="none" stroke="#cbd5e1" stroke-dasharray="5,4"/>
''')

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, cfg in DIAGRAMS.items():
        path = OUT / f"{name}.svg"
        path.write_text(generate(cfg), encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
