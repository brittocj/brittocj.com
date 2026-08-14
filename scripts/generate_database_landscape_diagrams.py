#!/usr/bin/env python3
"""Generate SVG diagrams for the 'From SQL to Vector Databases' blog post."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "blog"


def svg_header(w=1100, h=650):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img">
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 Z" fill="#505050"/>
    </marker>
    <marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 Z" fill="#3b82f6"/>
    </marker>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-opacity="0.12"/>
    </filter>
  </defs>
  <rect width="{w}" height="{h}" fill="#ffffff"/>
'''


def box(x, y, w, h, label, color="#3b82f6", fill="#eff6ff", font_size=11, sub=None, bold=True):
    text = f'<text x="{w/2}" y="{h/2 + 4}" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="{font_size}" font-weight="{"700" if bold else "600"}" fill="#1e293b">{label}</text>'
    if sub:
        text += f'<text x="{w/2}" y="{h/2 + 20}" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#64748b">{sub}</text>'
    return f'''
  <g transform="translate({x},{y})">
    <rect x="0" y="0" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{color}" stroke-width="1.5" filter="url(#shadow)"/>
    {text}
  </g>'''


def arrow(x1, y1, x2, y2, color="#505050", dash=None, width=1.5):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    marker = "url(#arrow-blue)" if color == "#3b82f6" else "url(#arrow)"
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{dash_attr} marker-end="{marker}"/>'


def title_text(text, y=36, size=20):
    return f'<text x="550" y="{y}" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="700" fill="#1e293b">{text}</text>'


def generate_evolution():
    """Database evolution timeline."""
    parts = [svg_header(1100, 420), title_text("The Database Evolution Journey")]
    stages = [
        ("SQL", "Relational", "#3b82f6", "#eff6ff"),
        ("NoSQL", "Flexible models", "#8b5cf6", "#f5f3ff"),
        ("Distributed", "Horizontal scale", "#f59e0b", "#fffbeb"),
        ("Cloud Managed", "Serverless ops", "#10b981", "#ecfdf5"),
        ("Data Warehouse", "Analytics", "#ef4444", "#fef2f2"),
        ("Search Engines", "Full-text", "#06b6d4", "#ecfeff"),
        ("Vector DB", "AI semantic", "#ec4899", "#fdf2f8"),
        ("AI-Native", "Data + LLM", "#6366f1", "#eef2ff"),
    ]
    x = 40
    w = 115
    gap = 12
    y = 120
    h = 90
    for i, (name, sub, color, fill) in enumerate(stages):
        parts.append(box(x, y, w, h, name, color, fill, 12, sub))
        if i < len(stages) - 1:
            parts.append(arrow(x + w, y + h/2, x + w + gap, y + h/2))
        x += w + gap
    parts.append(f'<text x="550" y="280" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="12" fill="#64748b">Each stage builds on the previous - from rigid tables to AI-native data platforms</text>')
    parts.append(f'<text x="550" y="320" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#94a3b8">The journey is not about replacement - it is about adding new capabilities</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_cache_aside():
    """Cache-aside / lazy caching architecture."""
    parts = [svg_header(1100, 400), title_text("Cache-Aside (Lazy Caching) Pattern")]
    parts.append(box(80, 140, 160, 70, "Browser", "#3b82f6", "#eff6ff", 13, "Client application"))
    parts.append(box(380, 140, 180, 70, "Application", "#8b5cf6", "#f5f3ff", 13, "Business logic"))
    parts.append(box(700, 60, 200, 70, "Redis Cache", "#ef4444", "#fef2f2", 13, "In-memory store"))
    parts.append(box(700, 240, 200, 70, "PostgreSQL", "#10b981", "#ecfdf5", 13, "System of record"))
    parts.append(arrow(240, 175, 380, 175, "#3b82f6", None, 2))
    parts.append(f'<text x="310" y="165" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#64748b">Request</text>')
    parts.append(arrow(560, 165, 700, 95, "#3b82f6", None, 2))
    parts.append(f'<text x="630" y="120" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#64748b">1. Check cache</text>')
    parts.append(arrow(700, 130, 560, 165, "#3b82f6", "5,4", 2))
    parts.append(f'<text x="630" y="150" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#64748b">2. Cache hit</text>')
    parts.append(arrow(560, 195, 700, 275, "#f59e0b", None, 2))
    parts.append(f'<text x="630" y="240" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#64748b">3. Cache miss → DB</text>')
    parts.append(arrow(700, 310, 560, 195, "#f59e0b", "5,4", 2))
    parts.append(f'<text x="630" y="330" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#64748b">4. Return data</text>')
    parts.append(arrow(700, 95, 700, 240, "#10b981", "5,4", 2))
    parts.append(f'<text x="720" y="170" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#64748b">5. Populate cache</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_rag():
    """RAG architecture."""
    parts = [svg_header(1100, 500), title_text("RAG - Retrieval-Augmented Generation")]
    stages = [
        ("User Question", "How does Kubernetes manage containers?", "#3b82f6", "#eff6ff"),
        ("Embedding Model", "Converts text → vector", "#8b5cf6", "#f5f3ff"),
        ("Vector Database", "Semantic similarity search", "#ec4899", "#fdf2f8"),
        ("Relevant Documents", "Top-k matches", "#f59e0b", "#fffbeb"),
        ("LLM", "Generates grounded answer", "#10b981", "#ecfdf5"),
        ("Answer", "Context-aware response", "#6366f1", "#eef2ff"),
    ]
    x = 80
    w = 140
    gap = 30
    y = 140
    h = 90
    for i, (name, sub, color, fill) in enumerate(stages):
        parts.append(box(x, y, w, h, name, color, fill, 12, sub))
        if i < len(stages) - 1:
            parts.append(arrow(x + w, y + h/2, x + w + gap, y + h/2, "#3b82f6", None, 2))
        x += w + gap
    parts.append(f'<text x="550" y="300" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">The LLM answers using retrieved context - reducing hallucinations and grounding responses in your data</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_sharding():
    """Database sharding diagram."""
    parts = [svg_header(1100, 450), title_text("Database Sharding - Horizontal Partitioning")]
    parts.append(box(420, 60, 260, 70, "Application", "#3b82f6", "#eff6ff", 14, "1 billion customers"))
    parts.append(box(420, 180, 260, 60, "Sharding Layer", "#8b5cf6", "#f5f3ff", 13, "customer_id % 3"))
    shards = [
        ("DB-01", "0 – 333M", "#10b981", "#ecfdf5"),
        ("DB-02", "334M – 666M", "#f59e0b", "#fffbeb"),
        ("DB-03", "667M – 1B", "#ef4444", "#fef2f2"),
    ]
    for i, (name, range_str, color, fill) in enumerate(shards):
        x = 80 + i * 330
        parts.append(box(x, 300, 260, 80, name, color, fill, 14, range_str))
        parts.append(arrow(550, 240, x + 130, 300, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="420" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Each shard holds a subset of data - enabling horizontal scale and failure isolation</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_replication():
    """Database replication diagram."""
    parts = [svg_header(1100, 380), title_text("Database Replication")]
    parts.append(box(420, 60, 260, 70, "Primary", "#3b82f6", "#eff6ff", 14, "Handles all writes"))
    replicas = [
        ("Replica 1", "Read traffic", "#10b981", "#ecfdf5"),
        ("Replica 2", "Read traffic", "#f59e0b", "#fffbeb"),
        ("Replica 3", "Read traffic", "#8b5cf6", "#f5f3ff"),
    ]
    for i, (name, sub, color, fill) in enumerate(replicas):
        x = 80 + i * 330
        parts.append(box(x, 220, 260, 70, name, color, fill, 13, sub))
        parts.append(arrow(550, 130, x + 130, 220, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="330" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Provides high availability, read scalability, and disaster recovery</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_read_replicas():
    """Read replicas diagram."""
    parts = [svg_header(1100, 400), title_text("Read Replicas - Scaling Read Workloads")]
    parts.append(box(420, 60, 260, 70, "Application", "#3b82f6", "#eff6ff", 14, "Read-heavy workload"))
    parts.append(box(80, 220, 260, 70, "Primary", "#10b981", "#ecfdf5", 13, "Writes"))
    parts.append(box(420, 220, 260, 70, "Replica 1", "#f59e0b", "#fffbeb", 13, "Reads"))
    parts.append(box(760, 220, 260, 70, "Replica 2", "#8b5cf6", "#f5f3ff", 13, "Reads"))
    parts.append(arrow(550, 130, 210, 220, "#3b82f6", None, 2))
    parts.append(arrow(550, 130, 550, 220, "#3b82f6", None, 2))
    parts.append(arrow(550, 130, 890, 220, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="330" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Typical for news sites, e-commerce, SaaS, and analytics dashboards</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_clustering():
    """Database clustering diagram."""
    parts = [svg_header(1100, 380), title_text("Database Clustering")]
    parts.append(box(420, 60, 260, 60, "Load Balancer", "#3b82f6", "#eff6ff", 13, "Distributes traffic"))
    dbs = [
        ("DB1", "#10b981", "#ecfdf5"),
        ("DB2", "#f59e0b", "#fffbeb"),
        ("DB3", "#8b5cf6", "#f5f3ff"),
    ]
    for i, (name, color, fill) in enumerate(dbs):
        x = 80 + i * 330
        parts.append(box(x, 200, 260, 70, name, color, fill, 14, "Cluster node"))
        parts.append(arrow(550, 120, x + 130, 200, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="320" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">High availability, replication, automatic failover, and horizontal scaling</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_oltp_olap():
    """OLTP vs OLAP architecture."""
    parts = [svg_header(1100, 480), title_text("OLTP → OLAP Pipeline")]
    parts.append(box(80, 60, 200, 70, "Application", "#3b82f6", "#eff6ff", 13, "Day-to-day ops"))
    parts.append(box(380, 60, 200, 70, "OLTP Database", "#10b981", "#ecfdf5", 13, "PostgreSQL / MySQL"))
    parts.append(box(680, 60, 200, 70, "CDC / Events", "#f59e0b", "#fffbeb", 13, "Change data capture"))
    parts.append(box(80, 220, 200, 70, "Data Lake", "#8b5cf6", "#f5f3ff", 13, "Raw storage"))
    parts.append(box(380, 220, 200, 70, "Data Warehouse", "#ef4444", "#fef2f2", 13, "BigQuery / Redshift"))
    parts.append(box(680, 220, 200, 70, "BI / Analytics", "#06b6d4", "#ecfeff", 13, "Dashboards"))
    parts.append(arrow(280, 95, 380, 95, "#3b82f6", None, 2))
    parts.append(arrow(580, 95, 680, 95, "#3b82f6", None, 2))
    parts.append(arrow(780, 130, 780, 220, "#3b82f6", None, 2))
    parts.append(arrow(280, 130, 180, 220, "#3b82f6", None, 2))
    parts.append(arrow(280, 255, 380, 255, "#3b82f6", None, 2))
    parts.append(arrow(580, 255, 680, 255, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="340" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">OLTP handles transactions; OLAP powers large-scale analysis and business intelligence</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_modern_architecture():
    """Modern enterprise AI application architecture."""
    parts = [svg_header(1100, 650), title_text("Modern Enterprise AI Application Architecture")]
    # Users
    parts.append(box(420, 30, 260, 50, "Users", "#3b82f6", "#eff6ff", 13))
    parts.append(box(420, 100, 260, 50, "API Gateway", "#8b5cf6", "#f5f3ff", 13))
    parts.append(box(420, 170, 260, 50, "Application", "#6366f1", "#eef2ff", 13))
    # Data stores
    parts.append(box(60, 280, 220, 60, "PostgreSQL", "#10b981", "#ecfdf5", 12, "Transactional data"))
    parts.append(box(440, 280, 220, 60, "Redis", "#ef4444", "#fef2f2", 12, "Caching"))
    parts.append(box(820, 280, 220, 60, "Object Storage", "#f59e0b", "#fffbeb", 12, "Documents"))
    # AI pipeline
    parts.append(box(820, 380, 220, 60, "Embedding Model", "#06b6d4", "#ecfeff", 12, "Text → vectors"))
    parts.append(box(820, 480, 220, 60, "Vector Database", "#ec4899", "#fdf2f8", 12, "Semantic search"))
    parts.append(box(820, 580, 220, 60, "LLM", "#6366f1", "#eef2ff", 12, "Answer generation"))
    # Arrows
    parts.append(arrow(550, 80, 550, 100, "#3b82f6", None, 2))
    parts.append(arrow(550, 150, 550, 170, "#3b82f6", None, 2))
    parts.append(arrow(420, 195, 170, 280, "#3b82f6", None, 2))
    parts.append(arrow(550, 220, 550, 280, "#3b82f6", None, 2))
    parts.append(arrow(680, 195, 930, 280, "#3b82f6", None, 2))
    parts.append(arrow(930, 340, 930, 380, "#3b82f6", None, 2))
    parts.append(arrow(930, 440, 930, 480, "#3b82f6", None, 2))
    parts.append(arrow(930, 540, 930, 580, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="640" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Polyglot persistence - the right database for each workload</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_ai_assistant():
    """Enterprise knowledge assistant architecture."""
    parts = [svg_header(1100, 600), title_text("Enterprise Knowledge Assistant")]
    stages = [
        ("Employee", "Asks a question", "#3b82f6", "#eff6ff"),
        ("LLM", "Understands intent", "#8b5cf6", "#f5f3ff"),
        ("Vector Search", "Finds relevant docs", "#ec4899", "#fdf2f8"),
        ("Graph Relationships", "Maps connections", "#f59e0b", "#fffbeb"),
        ("PostgreSQL Metadata", "Structured context", "#10b981", "#ecfdf5"),
        ("LLM", "Synthesizes answer", "#6366f1", "#eef2ff"),
        ("Answer", "Grounded response", "#06b6d4", "#ecfeff"),
    ]
    x = 60
    w = 130
    gap = 20
    y = 140
    h = 80
    for i, (name, sub, color, fill) in enumerate(stages):
        parts.append(box(x, y, w, h, name, color, fill, 11, sub))
        if i < len(stages) - 1:
            parts.append(arrow(x + w, y + h/2, x + w + gap, y + h/2, "#3b82f6", None, 2))
        x += w + gap
    parts.append(f'<text x="550" y="300" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Combining SQL + NoSQL + Vector Search + Graph + LLMs for AI-native applications</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_monitoring():
    """Monitoring architecture."""
    parts = [svg_header(1100, 380), title_text("Time-Series Monitoring Stack")]
    parts.append(box(80, 140, 200, 70, "Servers", "#3b82f6", "#eff6ff", 13, "Infrastructure"))
    parts.append(box(380, 140, 240, 70, "Prometheus / Collectors", "#8b5cf6", "#f5f3ff", 12, "Metrics scraping"))
    parts.append(box(700, 140, 220, 70, "Time-Series Database", "#f59e0b", "#fffbeb", 12, "InfluxDB / TimescaleDB"))
    parts.append(box(940, 140, 140, 70, "Grafana", "#10b981", "#ecfdf5", 13, "Dashboards"))
    parts.append(arrow(280, 175, 380, 175, "#3b82f6", None, 2))
    parts.append(arrow(620, 175, 700, 175, "#3b82f6", None, 2))
    parts.append(arrow(920, 175, 940, 175, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="280" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Used for monitoring, IoT, financial data, infrastructure metrics, and application telemetry</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_analytics_gcp():
    """GCP analytics architecture."""
    parts = [svg_header(1100, 400), title_text("Analytics Pipeline (Google Cloud)")]
    parts.append(box(80, 140, 200, 70, "Applications", "#3b82f6", "#eff6ff", 13, "Event sources"))
    parts.append(box(380, 140, 200, 70, "Pub/Sub", "#8b5cf6", "#f5f3ff", 13, "Event streaming"))
    parts.append(box(680, 140, 200, 70, "Data Processing", "#f59e0b", "#fffbeb", 13, "Dataflow / Dataproc"))
    parts.append(box(80, 280, 200, 70, "BigQuery", "#10b981", "#ecfdf5", 13, "Analytics warehouse"))
    parts.append(box(380, 280, 200, 70, "BI / Analytics", "#06b6d4", "#ecfeff", 13, "Looker / dashboards"))
    parts.append(arrow(280, 175, 380, 175, "#3b82f6", None, 2))
    parts.append(arrow(580, 175, 680, 175, "#3b82f6", None, 2))
    parts.append(arrow(780, 210, 780, 280, "#3b82f6", None, 2))
    parts.append(arrow(280, 210, 180, 280, "#3b82f6", None, 2))
    parts.append(arrow(280, 315, 380, 315, "#3b82f6", None, 2))
    parts.append("</svg>")
    return "\n".join(parts)


def generate_aws_architecture():
    """AWS reference architecture."""
    parts = [svg_header(1100, 500), title_text("Typical AWS Architecture")]
    parts.append(box(420, 30, 260, 50, "ALB", "#3b82f6", "#eff6ff", 13, "Application Load Balancer"))
    parts.append(box(420, 110, 260, 50, "ECS / EKS", "#8b5cf6", "#f5f3ff", 13, "Container platform"))
    services = [
        ("RDS PostgreSQL", "#10b981", "#ecfdf5"),
        ("ElastiCache", "#ef4444", "#fef2f2"),
        ("DynamoDB", "#f59e0b", "#fffbeb"),
        ("OpenSearch", "#06b6d4", "#ecfeff"),
        ("S3", "#6366f1", "#eef2ff"),
    ]
    for i, (name, color, fill) in enumerate(services):
        x = 60 + i * 200
        parts.append(box(x, 240, 180, 60, name, color, fill, 12))
        parts.append(arrow(550, 160, x + 90, 240, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="360" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Managed services for relational data, caching, NoSQL, search, and object storage</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_azure_architecture():
    """Azure reference architecture."""
    parts = [svg_header(1100, 500), title_text("Typical Azure Architecture")]
    parts.append(box(420, 30, 260, 50, "Azure Front Door", "#3b82f6", "#eff6ff", 13, "Global entry point"))
    parts.append(box(420, 110, 260, 50, "Application Gateway", "#8b5cf6", "#f5f3ff", 13, "L7 routing"))
    parts.append(box(420, 190, 260, 50, "AKS", "#6366f1", "#eef2ff", 13, "Kubernetes"))
    services = [
        ("Azure SQL", "#10b981", "#ecfdf5"),
        ("Cosmos DB", "#f59e0b", "#fffbeb"),
        ("Redis", "#ef4444", "#fef2f2"),
        ("Blob Storage", "#06b6d4", "#ecfeff"),
    ]
    for i, (name, color, fill) in enumerate(services):
        x = 60 + i * 250
        parts.append(box(x, 320, 220, 60, name, color, fill, 12))
        parts.append(arrow(550, 240, x + 110, 320, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="430" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Managed data services for SQL, NoSQL, caching, and storage</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_azure_ai():
    """Azure AI architecture."""
    parts = [svg_header(1100, 400), title_text("Azure AI Workload")]
    parts.append(box(80, 140, 200, 70, "AKS", "#3b82f6", "#eff6ff", 13, "Application platform"))
    parts.append(box(380, 140, 220, 70, "Azure AI Services", "#8b5cf6", "#f5f3ff", 12, "Cognitive APIs"))
    parts.append(box(680, 140, 200, 70, "Azure AI Search", "#ec4899", "#fdf2f8", 13, "Vector + keyword"))
    parts.append(box(920, 140, 160, 70, "LLM", "#10b981", "#ecfdf5", 13, "Generation"))
    parts.append(arrow(280, 175, 380, 175, "#3b82f6", None, 2))
    parts.append(arrow(600, 175, 680, 175, "#3b82f6", None, 2))
    parts.append(arrow(880, 175, 920, 175, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="280" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">AI Search combines vector and keyword search for RAG workloads</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_partitioning():
    """Database partitioning diagram."""
    parts = [svg_header(1100, 420), title_text("Database Partitioning")]
    parts.append(box(420, 40, 260, 60, "Orders Table", "#3b82f6", "#eff6ff", 13, "Logical table"))
    parts.append(box(80, 200, 260, 70, "Partition A", "#10b981", "#ecfdf5", 13, "2024 data"))
    parts.append(box(420, 200, 260, 70, "Partition B", "#f59e0b", "#fffbeb", 13, "2025 data"))
    parts.append(box(760, 200, 260, 70, "Partition C", "#8b5cf6", "#f5f3ff", 13, "2026 data"))
    parts.append(arrow(550, 100, 210, 200, "#3b82f6", None, 2))
    parts.append(arrow(550, 100, 550, 200, "#3b82f6", None, 2))
    parts.append(arrow(550, 100, 890, 200, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="330" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Range, hash, or list partitioning - queries only scan relevant partitions</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_wide_column():
    """Wide-column database model."""
    parts = [svg_header(1100, 400), title_text("Wide-Column Data Model")]
    parts.append(box(420, 40, 260, 60, "Partition Key", "#3b82f6", "#eff6ff", 13, "Distributes data"))
    cols = [
        ("Column A", "#10b981", "#ecfdf5"),
        ("Column B", "#f59e0b", "#fffbeb"),
        ("Column C", "#8b5cf6", "#f5f3ff"),
    ]
    for i, (name, color, fill) in enumerate(cols):
        x = 80 + i * 330
        parts.append(box(x, 200, 260, 70, name, color, fill, 13, "Column family"))
        parts.append(arrow(550, 100, x + 130, 200, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="330" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Designed for massive write throughput and horizontal scalability</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_graph():
    """Graph database model."""
    parts = [svg_header(1100, 400), title_text("Graph Data Model")]
    # Nodes
    parts.append(box(200, 140, 140, 60, "John", "#3b82f6", "#eff6ff", 13, "Person"))
    parts.append(box(480, 60, 140, 60, "Company A", "#10b981", "#ecfdf5", 12, "Organization"))
    parts.append(box(480, 240, 140, 60, "Company B", "#f59e0b", "#fffbeb", 12, "Organization"))
    parts.append(box(760, 140, 140, 60, "Mary", "#8b5cf6", "#f5f3ff", 13, "Person"))
    # Edges
    parts.append(arrow(340, 160, 480, 90, "#3b82f6", None, 2))
    parts.append(f'<text x="410" y="115" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#64748b">works_for</text>')
    parts.append(arrow(340, 180, 480, 270, "#3b82f6", None, 2))
    parts.append(f'<text x="410" y="235" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#64748b">works_for</text>')
    parts.append(arrow(340, 170, 760, 170, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="160" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="10" fill="#64748b">knows</text>')
    parts.append(f'<text x="550" y="340" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Nodes and relationships are first-class concepts - ideal for social networks, fraud detection, and knowledge graphs</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_vector_search():
    """Vector similarity search."""
    parts = [svg_header(1100, 400), title_text("Vector Similarity Search")]
    parts.append(box(80, 140, 240, 70, "Query Text", "#3b82f6", "#eff6ff", 13, '"How does Kubernetes manage containers?"'))
    parts.append(box(420, 140, 200, 70, "Embedding Model", "#8b5cf6", "#f5f3ff", 12, "Text → vector"))
    parts.append(box(720, 140, 260, 70, "Query Vector", "#ec4899", "#fdf2f8", 12, "[0.021, -0.182, 0.731, ...]"))
    parts.append(box(420, 280, 260, 70, "Vector Database", "#10b981", "#ecfdf5", 13, "Nearest neighbors"))
    parts.append(arrow(320, 175, 420, 175, "#3b82f6", None, 2))
    parts.append(arrow(620, 175, 720, 175, "#3b82f6", None, 2))
    parts.append(arrow(850, 210, 550, 280, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="390" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Finds documents semantically similar to the query - not just exact keyword matches</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def generate_events_pipeline():
    """Events pipeline to data warehouse."""
    parts = [svg_header(1100, 400), title_text("Events → Data Lake → Warehouse")]
    parts.append(box(80, 140, 200, 70, "Application Events", "#3b82f6", "#eff6ff", 13, "Kafka / Pub/Sub"))
    parts.append(box(380, 140, 200, 70, "Data Lake", "#8b5cf6", "#f5f3ff", 13, "Raw event storage"))
    parts.append(box(680, 140, 200, 70, "Data Warehouse", "#f59e0b", "#fffbeb", 13, "Curated analytics"))
    parts.append(box(920, 140, 160, 70, "BI Tools", "#10b981", "#ecfdf5", 13, "Dashboards"))
    parts.append(arrow(280, 175, 380, 175, "#3b82f6", None, 2))
    parts.append(arrow(580, 175, 680, 175, "#3b82f6", None, 2))
    parts.append(arrow(880, 175, 920, 175, "#3b82f6", None, 2))
    parts.append(f'<text x="550" y="280" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" fill="#64748b">Application events flow into a data lake, then into a warehouse for analytics</text>')
    parts.append("</svg>")
    return "\n".join(parts)


DIAGRAMS = {
    "database-evolution": generate_evolution,
    "cache-aside": generate_cache_aside,
    "rag-architecture": generate_rag,
    "database-sharding": generate_sharding,
    "database-replication": generate_replication,
    "read-replicas": generate_read_replicas,
    "database-clustering": generate_clustering,
    "oltp-olap-pipeline": generate_oltp_olap,
    "modern-ai-architecture": generate_modern_architecture,
    "ai-knowledge-assistant": generate_ai_assistant,
    "monitoring-stack": generate_monitoring,
    "analytics-gcp": generate_analytics_gcp,
    "aws-architecture": generate_aws_architecture,
    "azure-architecture": generate_azure_architecture,
    "azure-ai-workload": generate_azure_ai,
    "database-partitioning": generate_partitioning,
    "wide-column-model": generate_wide_column,
    "graph-model": generate_graph,
    "vector-search": generate_vector_search,
    "events-pipeline": generate_events_pipeline,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        path = OUT / f"{name}.svg"
        path.write_text(fn(), encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()