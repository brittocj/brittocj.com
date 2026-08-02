#!/usr/bin/env python3
"""Update blog: cloud architecture articles, career-aligned dates, nav fixes."""

import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
ASSETS = os.path.join(ROOT, "assets", "blog")

NAV_OLD = """        <li><a href="../../index.html#certifications">Certifications</a></li>
        <li><a href="../index.html#contact" class="nav__cta">Contact</a></li>"""

NAV_NEW = """        <li><a href="../../index.html#certifications">Certifications</a></li>
        <li><a href="../">Blog</a></li>
        <li><a href="../index.html#contact" class="nav__cta">Contact</a></li>"""

NAV_INDEX_OLD = """        <li><a href="../index.html#certifications">Certifications</a></li>
        <li><a href="../index.html#contact" class="nav__cta">Contact</a></li>"""

NAV_INDEX_NEW = """        <li><a href="../index.html#certifications">Certifications</a></li>
        <li><a href="./" class="active">Blog</a></li>
        <li><a href="../index.html#contact" class="nav__cta">Contact</a></li>"""

# Career-aligned dates (newest first on index). sort_key = YYYYMMDD
ARTICLES = [
    {"slug": "agentic-ai-in-india", "tag": "Featured", "title": "My Vision for the Future of Agentic AI in India",
     "excerpt": "Exploring how Agentic AI can transform healthcare, education, governance, and agriculture across India with inclusive innovation.",
     "date_short": "Jul 17, 2026", "date_full": "July 17, 2026", "read_time": "8 min", "sort_key": 20260717},
    {"slug": "linux-fundamentals", "tag": "Linux", "title": "Linux Fundamentals: The Foundation Every Cloud Engineer Needs",
     "excerpt": "Every Kubernetes node, every EC2 instance, every containerized workload. Underneath it all, Linux is running the show.",
     "date_short": "Oct 21, 2013", "date_full": "October 21, 2013", "read_time": "15 min", "sort_key": 20131021},
    {"slug": "sql-vs-nosql", "tag": "Database", "title": "SQL vs. NoSQL: Choosing the Right Database for Your Use Case",
     "excerpt": "Evaluation criteria for relational databases, document stores, time-series, and graph databases.",
     "date_short": "Mar 14, 2014", "date_full": "March 14, 2014", "read_time": "3 min", "sort_key": 20140314},
    {"slug": "monolith-to-microservices", "tag": "Microservices", "title": "From Monolith to Microservices: A Pragmatic Migration Strategy",
     "excerpt": "Planning and executing microservices adoption without the operational chaos.",
     "date_short": "Aug 27, 2014", "date_full": "August 27, 2014", "read_time": "4 min", "sort_key": 20140827},
    {"slug": "on-call-excellence", "tag": "Incident Management", "title": "On-Call Excellence: Building Effective Incident Response",
     "excerpt": "Runbooks, blameless postmortems, and creating sustainable on-call rotations.",
     "date_short": "Nov 12, 2015", "date_full": "November 12, 2015", "read_time": "4 min", "sort_key": 20151112},
    {"slug": "devops-culture-beyond-tools", "tag": "DevOps Culture", "title": "Building a DevOps Culture: Beyond Tools and Automation",
     "excerpt": "Organizational change, breaking silos, and fostering shared responsibility for production.",
     "date_short": "Jun 8, 2016", "date_full": "June 8, 2016", "read_time": "5 min", "sort_key": 20160608},
    {"slug": "iac-best-practices", "tag": "Infrastructure as Code", "title": "IaC Best Practices: Terraform, CloudFormation, and Beyond",
     "excerpt": "State management, modularity, testing, and GitOps integration for infrastructure code.",
     "date_short": "Oct 31, 2016", "date_full": "October 31, 2016", "read_time": "5 min", "sort_key": 20161031},
    {"slug": "cloud-networking-vpcs", "tag": "Networking", "title": "Understanding Cloud Networking: VPCs, Subnets, and Routing",
     "excerpt": "Network architecture patterns, VPC design, and connectivity between cloud and on-premises.",
     "date_short": "Feb 6, 2017", "date_full": "February 6, 2017", "read_time": "5 min", "sort_key": 20170206},
    {"slug": "testing-infrastructure", "tag": "Testing", "title": "Testing Infrastructure: Unit, Integration, and End-to-End Tests",
     "excerpt": "Building test pyramids, chaos engineering, and ensuring infrastructure reliability.",
     "date_short": "Apr 4, 2017", "date_full": "April 4, 2017", "read_time": "4 min", "sort_key": 20170404},
    {"slug": "observability-vs-monitoring", "tag": "Observability", "title": "Observability vs. Monitoring: Why the Distinction Matters",
     "excerpt": "Understanding logs, metrics, traces, and how to build truly observable systems.",
     "date_short": "Sep 19, 2017", "date_full": "September 19, 2017", "read_time": "5 min", "sort_key": 20170919},
    {"slug": "microservices-on-aws-eks", "tag": "AWS", "title": "Microservices Architecture on Amazon EKS",
     "excerpt": "Reference architecture for running microservices on Amazon EKS with ALB ingress, ECR, and managed AWS data services.",
     "date_short": "Jul 9, 2018", "date_full": "July 9, 2018", "read_time": "5 min", "sort_key": 20180709, "new": True},
    {"slug": "serverless-when-to-use", "tag": "Serverless", "title": "Serverless Computing: When and When Not to Use It",
     "excerpt": "Evaluating serverless vs. containers, cold start challenges, and cost implications.",
     "date_short": "Nov 2, 2018", "date_full": "November 2, 2018", "read_time": "4 min", "sort_key": 20181102},
    {"slug": "microservices-on-azure-aks", "tag": "Azure", "title": "Microservices Architecture on Azure Kubernetes Service",
     "excerpt": "How to design a production AKS platform with ingress, Azure Pipelines, managed data services, and Entra ID integration.",
     "date_short": "May 16, 2019", "date_full": "May 16, 2019", "read_time": "5 min", "sort_key": 20190516, "new": True},
    {"slug": "gitops-declarative-infrastructure", "tag": "DevOps", "title": "GitOps: Declarative Infrastructure for Modern Teams",
     "excerpt": "How GitOps principles enable consistent, auditable, and automated infrastructure deployments at scale.",
     "date_short": "Oct 22, 2019", "date_full": "October 22, 2019", "read_time": "5 min", "sort_key": 20191022},
    {"slug": "api-governance-at-scale", "tag": "API Management", "title": "API Governance and Management at Scale",
     "excerpt": "Implementing API standards, versioning strategies, and developer experience considerations.",
     "date_short": "Feb 11, 2020", "date_full": "February 11, 2020", "read_time": "3 min", "sort_key": 20200211},
    {"slug": "kubernetes-networking-cni", "tag": "Kubernetes", "title": "Kubernetes Networking: Understanding CNI Plugins",
     "excerpt": "Deep dive into Container Networking Interface, overlay networks, and service mesh considerations.",
     "date_short": "Jun 3, 2020", "date_full": "June 3, 2020", "read_time": "5 min", "sort_key": 20200603},
    {"slug": "microservices-on-gcp-gke", "tag": "Google Cloud", "title": "Microservices Architecture on Google Kubernetes Engine",
     "excerpt": "Building resilient microservices on GKE with Cloud Load Balancing, Artifact Registry, and managed Google Cloud data services.",
     "date_short": "Sep 14, 2020", "date_full": "September 14, 2020", "read_time": "5 min", "sort_key": 20200914, "new": True},
    {"slug": "zero-trust-architecture", "tag": "Security", "title": "Zero Trust Architecture in Cloud Environments",
     "excerpt": "Implementing zero-trust principles for identity, access control, and network security at enterprise scale.",
     "date_short": "Aug 15, 2021", "date_full": "August 15, 2021", "read_time": "4 min", "sort_key": 20210815},
    {"slug": "building-internal-developer-platforms", "tag": "Platform Engineering", "title": "Building Internal Developer Platforms (IDP)",
     "excerpt": "Creating self-service infrastructure and standardized deployment platforms that empower development teams.",
     "date_short": "Mar 25, 2021", "date_full": "March 25, 2021", "read_time": "5 min", "sort_key": 20210325},
    {"slug": "mlops-operationalizing-models", "tag": "AI/MLOps", "title": "MLOps: Operationalizing Machine Learning Models",
     "excerpt": "Model training, validation, deployment, monitoring, and continuous improvement cycles.",
     "date_short": "Dec 7, 2021", "date_full": "December 7, 2021", "read_time": "4 min", "sort_key": 20211207},
    {"slug": "microservices-on-oci-oke", "tag": "Oracle Cloud", "title": "Microservices Architecture on Oracle Kubernetes Engine",
     "excerpt": "Deploying microservices on OKE with OCI Load Balancer, OCIR, Autonomous Database, and OCI Vault for enterprise workloads.",
     "date_short": "Apr 18, 2022", "date_full": "April 18, 2022", "read_time": "5 min", "sort_key": 20220418, "new": True},
    {"slug": "rto-rpo-business-continuity", "tag": "Disaster Recovery", "title": "RTO and RPO: Planning for Business Continuity",
     "excerpt": "Designing resilient architectures with recovery time and recovery point objectives in mind.",
     "date_short": "Sep 8, 2022", "date_full": "September 8, 2022", "read_time": "4 min", "sort_key": 20220908},
    {"slug": "multi-cloud-strategies", "tag": "Cloud Architecture", "title": "Designing Multi-Cloud Strategies for Enterprise Scale",
     "excerpt": "Best practices for building resilient, cost-effective multi-cloud architectures across AWS, Azure, GCP, and OCI.",
     "date_short": "Nov 30, 2022", "date_full": "November 30, 2022", "read_time": "5 min", "sort_key": 20221130},
    {"slug": "cloud-cost-optimization", "tag": "Cloud Cost", "title": "Cloud Cost Optimization: Beyond Just Shutting Down Resources",
     "excerpt": "Strategic approaches to FinOps, reserved instances, and building cost-conscious cloud cultures.",
     "date_short": "Apr 6, 2023", "date_full": "April 6, 2023", "read_time": "5 min", "sort_key": 20230406},
    {"slug": "data-pipelines-etl", "tag": "Data Engineering", "title": "Data Pipelines and ETL: Modern Approaches",
     "excerpt": "Stream processing, batch processing, data warehousing, and real-time analytics.",
     "date_short": "Jul 21, 2023", "date_full": "July 21, 2023", "read_time": "3 min", "sort_key": 20230721},
    {"slug": "edge-computing-sovereign-infrastructure", "tag": "Edge Computing", "title": "Edge Computing and the Future of Sovereign Infrastructure",
     "excerpt": "Distributed computing at the edge, data residency, and building sovereign cloud appliances.",
     "date_short": "Oct 9, 2023", "date_full": "October 9, 2023", "read_time": "5 min", "sort_key": 20231009},
    {"slug": "scalable-ml-pipelines", "tag": "AI/ML", "title": "Building Scalable ML Pipelines with Cloud Infrastructure",
     "excerpt": "Architecture patterns for ML workflows, data processing, and model serving in cloud-native environments.",
     "date_short": "Aug 22, 2024", "date_full": "August 22, 2024", "read_time": "4 min", "sort_key": 20240822},
    {"slug": "compliance-as-code", "tag": "Compliance", "title": "Compliance as Code: Automating Governance and Audits",
     "excerpt": "Policy as Code, automated compliance checks, and maintaining audit trails.",
     "date_short": "May 14, 2024", "date_full": "May 14, 2024", "read_time": "3 min", "sort_key": 20240514},
    {"slug": "performance-optimization", "tag": "Performance", "title": "Performance Optimization: From Application to Infrastructure",
     "excerpt": "Profiling, bottleneck identification, and scaling strategies at each layer.",
     "date_short": "Nov 18, 2024", "date_full": "November 18, 2024", "read_time": "4 min", "sort_key": 20241118},
    {"slug": "contributing-open-source", "tag": "Open Source", "title": "Contributing to Open Source: A Guide for Cloud Engineers",
     "excerpt": "Finding the right projects, making meaningful contributions, and building community.",
     "date_short": "Feb 3, 2024", "date_full": "February 3, 2024", "read_time": "3 min", "sort_key": 20240203},
    {"slug": "growing-cloud-career", "tag": "Career", "title": "Growing Your Cloud Engineering Career: Skills and Mindset",
     "excerpt": "Continuous learning, certifications, building a strong professional network, and thought leadership.",
     "date_short": "Mar 5, 2025", "date_full": "March 5, 2025", "read_time": "3 min", "sort_key": 20250305},
    {"slug": "green-cloud-sustainable-computing", "tag": "Sustainability", "title": "Green Cloud: Sustainable Computing and Carbon-Aware Architectures",
     "excerpt": "Building environmentally responsible infrastructure, energy-efficient operations, and sustainability metrics.",
     "date_short": "Jan 20, 2022", "date_full": "January 20, 2022", "read_time": "3 min", "sort_key": 20220120},
    {"slug": "technology-trends-2026", "tag": "Innovation", "title": "Technology Trends 2026: What's Shaping the Cloud Landscape",
     "excerpt": "AI integration, quantum computing, edge computing, and emerging architectural patterns.",
     "date_short": "Oct 28, 2025", "date_full": "October 28, 2025", "read_time": "4 min", "sort_key": 20251028},
    {"slug": "leading-technical-teams", "tag": "Leadership", "title": "Leading Technical Teams: From IC to Manager",
     "excerpt": "Transitioning roles, mentoring, delegation, and building high-performing teams.",
     "date_short": "Jun 12, 2025", "date_full": "June 12, 2025", "read_time": "5 min", "sort_key": 20250612},
]

CLOUD_ARTICLES = {
    "microservices-on-aws-eks": {
        "description": "Reference architecture for microservices on Amazon EKS with ALB, ECR, and managed AWS services.",
        "cloud": "AWS",
        "svg": "aws-eks-architecture.svg",
        "caption": "Microservices architecture on Amazon EKS",
        "context": "After Amazon EKS reached general availability in 2018, we began standardizing Kubernetes deployments for enterprise clients at VF Interactive. This reference design reflects patterns I have applied across production AWS environments.",
        "sections": [
            ("Traffic flow", "Client applications connect through an <strong>Application Load Balancer</strong> with a public IP. The ALB routes HTTP traffic to an <strong>NGINX Ingress Controller</strong> running in a frontend namespace inside the EKS cluster. The ingress distributes requests to backend microservices based on path or host rules."),
            ("Microservice layout", "Backend services run in a dedicated namespace. <code>microservice1</code> handles API gateway responsibilities, <code>microservice2</code> coordinates business logic, and <code>microservice3</code> through <code>microservice5</code> own domain-specific data access. Each service scales independently through Kubernetes Deployments and Horizontal Pod Autoscalers."),
            ("CI/CD and images", "<strong>AWS CodePipeline</strong> and <strong>CodeBuild</strong> build container images on each merge. Images push to <strong>Amazon ECR</strong>. <strong>Helm</strong> charts deploy releases into EKS namespaces. The cluster pulls images from ECR using IAM roles for service accounts."),
            ("Data and messaging", "External data stores sit outside the cluster: <strong>Amazon RDS</strong> for relational data, <strong>DynamoDB</strong> for key-value workloads, <strong>ElastiCache</strong> for caching, and <strong>Amazon SQS</strong> for asynchronous messaging between services."),
            ("Security and operations", "<strong>IAM</strong> provides RBAC integration through IRSA. <strong>AWS Secrets Manager</strong> stores credentials. <strong>Amazon VPC CNI</strong> assigns pod IPs from your VPC. <strong>CloudWatch</strong> and <strong>X-Ray</strong> deliver logs, metrics, and distributed tracing."),
        ],
        "tags": ["AWS", "EKS", "Kubernetes", "Microservices", "ALB", "ECR", "Helm"],
    },
    "microservices-on-azure-aks": {
        "description": "Production AKS reference architecture with ingress, Azure DevOps, and managed Azure data services.",
        "cloud": "Azure",
        "svg": "azure-aks-architecture.svg",
        "caption": "Microservices architecture on Azure Kubernetes Service",
        "context": "While leading cloud architecture at VF Interactive, I designed several AKS platforms for clients moving from VM-based deployments to Kubernetes. The layout below mirrors Microsoft's recommended enterprise pattern with namespaces, managed services, and GitOps-ready CI/CD.",
        "sections": [
            ("Traffic flow", "Client apps reach a <strong>public IP</strong> on an <strong>Azure Load Balancer</strong>, which forwards traffic to an <strong>NGINX Ingress</strong> controller in the frontend namespace. Ingress rules route requests to backend microservices without exposing individual pods publicly."),
            ("Microservice layout", "The backend namespace hosts a chain of services: <code>microservice1</code> through <code>microservice5</code> with clear separation between API, orchestration, and data layers. <strong>Azure CNI powered by Cilium</strong> provides performant pod networking and network policy enforcement."),
            ("CI/CD and images", "<strong>Azure Pipelines</strong> builds and tests each service. <strong>Helm</strong> deploys chart releases into AKS. Container images push to <strong>Azure Container Registry</strong> and pull into the cluster on deployment."),
            ("Data and messaging", "Managed Azure services handle persistence: <strong>Azure Cosmos DB</strong> for globally distributed document data, <strong>Azure Managed Redis</strong> for caching, and <strong>Azure Service Bus</strong> for reliable async messaging."),
            ("Security and operations", "<strong>Microsoft Entra ID</strong> integrates with Kubernetes RBAC. <strong>Managed identities</strong> access <strong>Azure Key Vault</strong> without embedded secrets. <strong>Log Analytics</strong>, <strong>Application Insights</strong>, and <strong>Azure Monitor</strong> provide unified observability."),
        ],
        "tags": ["Azure", "AKS", "Kubernetes", "Microservices", "Azure DevOps", "Helm", "Entra ID"],
    },
    "microservices-on-gcp-gke": {
        "description": "GKE microservices reference architecture with Cloud Load Balancing, Artifact Registry, and managed GCP services.",
        "cloud": "Google Cloud",
        "svg": "gcp-gke-architecture.svg",
        "caption": "Microservices architecture on Google Kubernetes Engine",
        "context": "Google Kubernetes Engine was an early managed Kubernetes option, and at VF Interactive we adopted GKE for workloads that benefited from tight integration with BigQuery, Pub/Sub, and Cloud SQL. This architecture reflects a production-ready GKE layout from 2020 onward.",
        "sections": [
            ("Traffic flow", "Users connect through <strong>Cloud Load Balancing</strong> with a global anycast IP. Traffic enters an <strong>Ingress</strong> controller in the frontend namespace, which routes to backend microservices based on URL paths and hostnames."),
            ("Microservice layout", "Services run in isolated namespaces with <code>microservice1</code> acting as the edge API, <code>microservice2</code> handling orchestration, and <code>microservice3</code> to <code>microservice5</code> owning data access. <strong>VPC-native GKE</strong> networking assigns each pod a routable IP from your VPC subnet."),
            ("CI/CD and images", "<strong>Cloud Build</strong> triggers on commits to build and scan images. Artifacts land in <strong>Artifact Registry</strong>. <strong>Helm</strong> or <strong>Config Sync</strong> deploys workloads. Workload Identity lets pods authenticate to GCP APIs without static keys."),
            ("Data and messaging", "External stores include <strong>Cloud SQL</strong> for relational data, <strong>Firestore</strong> for document workloads, <strong>Memorystore</strong> for Redis caching, and <strong>Pub/Sub</strong> for event-driven communication between services."),
            ("Security and operations", "<strong>Cloud IAM</strong> and <strong>Workload Identity</strong> enforce least-privilege access. <strong>Secret Manager</strong> stores sensitive configuration. <strong>Cloud Monitoring</strong> and <strong>Cloud Trace</strong> deliver metrics, logs, and request tracing."),
        ],
        "tags": ["GCP", "GKE", "Kubernetes", "Microservices", "Cloud Build", "Artifact Registry", "Helm"],
    },
    "microservices-on-oci-oke": {
        "description": "OKE microservices reference architecture with OCI Load Balancer, OCIR, and Autonomous Database.",
        "cloud": "Oracle Cloud",
        "svg": "oci-oke-architecture.svg",
        "caption": "Microservices architecture on Oracle Kubernetes Engine",
        "context": "As OCI matured, VF Interactive began delivering OKE-based platforms for clients with Oracle database estates and data residency requirements. This design combines Kubernetes-native microservices with OCI managed services.",
        "sections": [
            ("Traffic flow", "Client traffic hits an <strong>OCI Load Balancer</strong> public IP, which forwards to an <strong>NGINX Ingress</strong> controller in the frontend namespace. Ingress rules distribute requests across backend microservices inside the OKE cluster."),
            ("Microservice layout", "Backend namespaces host <code>microservice1</code> through <code>microservice5</code> with the same API-orchestration-data layering used on other clouds. <strong>OCI VCN-Native Pod Networking</strong> integrates pods directly into your virtual cloud network."),
            ("CI/CD and images", "<strong>OCI DevOps</strong> pipelines build, test, and deploy services. Images push to <strong>Oracle Container Image Registry (OCIR)</strong>. <strong>Helm</strong> charts promote releases across dev, staging, and production clusters."),
            ("Data and messaging", "Persistence uses <strong>Autonomous Database</strong> for Oracle and compatible SQL workloads, <strong>OCI Cache</strong> with Redis for session and query caching, and <strong>OCI Streaming</strong> for event-driven integration between services."),
            ("Security and operations", "<strong>OCI IAM</strong> controls cluster and API access. <strong>OCI Vault</strong> manages secrets and encryption keys. <strong>OCI Monitoring</strong>, <strong>Logging</strong>, and <strong>APM</strong> provide operational visibility across the stack."),
        ],
        "tags": ["OCI", "OKE", "Kubernetes", "Microservices", "OCIR", "Autonomous Database", "Helm"],
    },
}


def svg_box(x, y, w, h, label, fill="#e8f4fd", stroke="#0078d4", sublabel=None):
    lines = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    if sublabel:
        lines += f'<text x="{x + w/2}" y="{y + h/2 - 4}" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" font-weight="600" fill="#1e293b">{label}</text>'
        lines += f'<text x="{x + w/2}" y="{y + h/2 + 12}" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#475569">{sublabel}</text>'
    else:
        lines += f'<text x="{x + w/2}" y="{y + h/2 + 4}" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11" font-weight="600" fill="#1e293b">{label}</text>'
    return lines


def svg_arrow(x1, y1, x2, y2, dashed=False):
    dash = 'stroke-dasharray="5,4"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow)" {dash}/>'


def build_architecture_svg(config):
    """Generate cloud-specific architecture SVG."""
    c = config
    w, h = 900, 520
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{c["title"]}">',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#64748b"/></marker></defs>',
        f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
        # Client
        svg_box(30, 200, 90, 50, "Client apps"),
        # LB
        svg_box(160, 195, 110, 60, c["lb"], sublabel="Public IP"),
        svg_arrow(120, 225, 160, 225),
        # Cluster boundary
        f'<rect x="310" y="60" width="340" height="280" rx="6" fill="none" stroke="#0078d4" stroke-width="2" stroke-dasharray="8,5"/>',
        f'<text x="320" y="52" font-family="Segoe UI,Arial,sans-serif" font-size="12" font-weight="700" fill="#0078d4">{c["cluster"]}</text>',
        # Frontend ns
        f'<rect x="325" y="75" width="145" height="95" rx="4" fill="#f1f5f9" stroke="#94a3b8"/>',
        f'<text x="335" y="92" font-family="Segoe UI,Arial,sans-serif" font-size="10" font-weight="600" fill="#475569">Front end Namespace</text>',
        svg_box(340, 100, 115, 55, "NGINX Ingress"),
        # Backend ns
        f'<rect x="485" y="75" width="150" height="250" rx="4" fill="#f1f5f9" stroke="#94a3b8"/>',
        f'<text x="495" y="92" font-family="Segoe UI,Arial,sans-serif" font-size="10" font-weight="600" fill="#475569">Back end Namespace</text>',
    ]
    parts.append(svg_arrow(270, 225, 340, 130))
    # Microservices chain
    ms_y = 110
    for i, name in enumerate(["microservice1", "microservice2", "microservice3", "microservice4", "microservice5"]):
        y = ms_y + i * 42
        bw = 120 if i < 2 else 100
        bx = 500 if i < 2 else 510
        parts.append(svg_box(bx, y, bw, 32, name, fill="#dbeafe" if i < 2 else "#e0e7ff", stroke="#3b82f6"))
        if i == 0:
            parts.append(svg_arrow(455, 128, 500, y + 16))
        elif i == 1:
            parts.append(svg_arrow(560, ms_y + 16, 560, y + 16))
        elif i == 2:
            parts.append(svg_arrow(620, ms_y + 42 + 16, 510, y + 16))
    # CNI
    parts.append(svg_box(370, 310, 200, 35, c["cni"], fill="#fef3c7", stroke="#d97706"))
    # External data stores
    parts.append(f'<text x="700" y="80" font-family="Segoe UI,Arial,sans-serif" font-size="11" font-weight="700" fill="#475569">External data stores</text>')
    for i, store in enumerate(c["stores"]):
        parts.append(svg_box(680, 95 + i * 52, 190, 40, store, fill="#f0fdf4", stroke="#16a34a"))
        parts.append(svg_arrow(635, 200, 680, 115 + i * 52 + 20))
    # CI/CD
    parts.append(svg_box(30, 400, 130, 55, c["cicd"], fill="#ede9fe", stroke="#7c3aed"))
    parts.append(svg_box(180, 410, 120, 40, c["registry"], fill="#ede9fe", stroke="#7c3aed"))
    parts.append(svg_arrow(160, 428, 180, 430))
    parts.append(svg_arrow(110, 400, 380, 340))
    parts.append(f'<text x="200" y="395" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#64748b">Image push</text>')
    parts.append(svg_arrow(300, 430, 370, 350, dashed=True))
    parts.append(f'<text x="310" y="385" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#64748b">Image pull</text>')
    parts.append(f'<text x="50" y="392" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#64748b">Helm</text>')
    # Bottom row security/monitoring
    bottom = c["bottom"]
    bx = 30
    for item in bottom:
        parts.append(svg_box(bx, 460, 115, 40, item["label"], fill=item.get("fill", "#f8fafc"), stroke="#64748b", sublabel=item.get("sub")))
        bx += 125
    # RBAC arrow
    if c.get("rbac"):
        parts.append(svg_arrow(480, 370, 480, 460))
        parts.append(f'<text x="490" y="420" font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#64748b">{c["rbac"]}</text>')
    parts.append('</svg>')
    return "\n".join(parts)


SVG_CONFIGS = {
    "aws-eks-architecture.svg": {
        "title": "Microservices on Amazon EKS",
        "lb": "Application Load Balancer",
        "cluster": "Amazon EKS",
        "cni": "Amazon VPC CNI",
        "cicd": "AWS CodePipeline",
        "registry": "Amazon ECR",
        "stores": ["Amazon RDS", "DynamoDB", "ElastiCache", "Amazon SQS"],
        "rbac": "IAM / IRSA",
        "bottom": [
            {"label": "IAM"},
            {"label": "Secrets Manager"},
            {"label": "CloudWatch"},
            {"label": "X-Ray"},
            {"label": "VPC"},
        ],
    },
    "azure-aks-architecture.svg": {
        "title": "Microservices on Azure AKS",
        "lb": "Azure Load Balancer",
        "cluster": "Azure Kubernetes Service",
        "cni": "Azure CNI (Cilium)",
        "cicd": "Azure Pipelines",
        "registry": "Azure Container Registry",
        "stores": ["Azure Cosmos DB", "Azure Managed Redis", "Azure Service Bus"],
        "rbac": "Entra ID RBAC",
        "bottom": [
            {"label": "Microsoft Entra ID"},
            {"label": "Managed identities"},
            {"label": "Key Vault"},
            {"label": "Log Analytics"},
            {"label": "Azure Monitor"},
        ],
    },
    "gcp-gke-architecture.svg": {
        "title": "Microservices on Google GKE",
        "lb": "Cloud Load Balancing",
        "cluster": "Google Kubernetes Engine",
        "cni": "VPC-native Pod networking",
        "cicd": "Cloud Build",
        "registry": "Artifact Registry",
        "stores": ["Cloud SQL", "Firestore", "Memorystore", "Pub/Sub"],
        "rbac": "Cloud IAM",
        "bottom": [
            {"label": "Cloud IAM"},
            {"label": "Secret Manager"},
            {"label": "Cloud Monitoring"},
            {"label": "Cloud Trace"},
            {"label": "VPC Network"},
        ],
    },
    "oci-oke-architecture.svg": {
        "title": "Microservices on Oracle OKE",
        "lb": "OCI Load Balancer",
        "cluster": "Oracle Kubernetes Engine",
        "cni": "VCN-Native Pod Networking",
        "cicd": "OCI DevOps",
        "registry": "OCIR",
        "stores": ["Autonomous DB", "OCI Cache", "OCI Streaming"],
        "rbac": "OCI IAM RBAC",
        "bottom": [
            {"label": "OCI IAM"},
            {"label": "OCI Vault"},
            {"label": "OCI Monitoring"},
            {"label": "OCI Logging"},
            {"label": "VCN"},
        ],
    },
}


def article_html(meta, article_info):
    slug = meta["slug"]
    info = article_info
    sections_html = "\n".join(
        f"        <h2>{title}</h2>\n        <p>{body}</p>" for title, body in info["sections"]
    )
    tags_html = "\n".join(f'            <span class="blog-tag">{t}</span>' for t in info["tags"])
    diagram = f'''        <figure class="blog-architecture">
          <img src="../../assets/blog/{info["svg"]}" alt="{info["caption"]}" width="900" height="520" loading="lazy">
          <figcaption>{info["caption"]}</figcaption>
        </figure>'''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{info['description']}">
  <meta name="author" content="Antony Britto C J">
  <title>{meta['title']} | Antony Britto C J</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../styles.css">
  <link rel="stylesheet" href="../post.css">
  <link rel="icon" type="image/png" href="../../assets/favicon.png">
</head>
<body>
  <nav class="nav" id="nav">
    <div class="nav__inner container">
      <a href="../../index.html" class="nav__logo">AB<span class="nav__logo-accent">.</span></a>
      <button class="nav__toggle" id="navToggle" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav__links" id="navLinks">
        <li><a href="../../index.html#about">About</a></li>
        <li><a href="../../index.html#expertise">Expertise</a></li>
        <li><a href="../../index.html#experience">Experience</a></li>
        <li><a href="../../index.html#projects">Projects</a></li>
        <li><a href="../../index.html#certifications">Certifications</a></li>
        <li><a href="../">Blog</a></li>
        <li><a href="../index.html#contact" class="nav__cta">Contact</a></li>
      </ul>
    </div>
  </nav>

  <section class="blog-post">
    <div class="container">
      <article class="blog-content">
        <div class="blog-header">
          <h1 class="blog-title">{meta['title']}</h1>
          <div class="blog-meta">
            <div class="blog-meta-item">📅 {meta['date_full']}</div>
            <div class="blog-meta-item">⏱️ {meta['read_time']} read</div>
          </div>
        </div>

        <p class="blog-lead">{meta['excerpt']}</p>

        <p>{info['context']}</p>

{diagram}

{sections_html}

        <div class="blog-tags">
          <div class="blog-tags-title">Topics &amp; Tags</div>
          <div class="blog-tags-list">
{tags_html}
          </div>
        </div>

        <div class="blog-nav">
          <a href="../">← Back to All Posts</a>
        </div>
      </article>
    </div>
  </section>

  <script src="../../script.js"></script>
</body>
</html>
"""


def update_article_dates():
    for meta in ARTICLES:
        path = os.path.join(BLOG, meta["slug"], "index.html")
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r'<div class="blog-meta-item">📅 [^<]+</div>',
            f'<div class="blog-meta-item">📅 {meta["date_full"]}</div>',
            content,
            count=1,
        )
        content = re.sub(
            r'<div class="blog-meta-item">⏱️ [^<]+</div>',
            f'<div class="blog-meta-item">⏱️ {meta["read_time"]} read</div>',
            content,
            count=1,
        )
        if NAV_OLD in content:
            content = content.replace(NAV_OLD, NAV_NEW)
        elif "Blog</a></li>" not in content and "../index.html#certifications" in content:
            content = content.replace(
                '<li><a href="../index.html#certifications">Certifications</a></li>\n        <li><a href="../index.html#contact"',
                '<li><a href="../index.html#certifications">Certifications</a></li>\n        <li><a href="../">Blog</a></li>\n        <li><a href="../index.html#contact"',
            )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def regenerate_blog_index():
    sorted_articles = sorted(ARTICLES, key=lambda a: a["sort_key"], reverse=True)
    cards = []
    for a in sorted_articles:
        featured = 'Featured' if a.get('tag') == 'Featured' else a['tag']
        cards.append(f"""        <a href="{a['slug']}/" class="blog-card">
          <span class="blog-card-tag">{featured}</span>
          <h2 class="blog-card-title">{a['title']}</h2>
          <p class="blog-card-excerpt">{a['excerpt']}</p>
          <div class="blog-card-meta">
            <span class="blog-card-date">📅 {a['date_short']}</span>
            <span class="blog-card-readtime">{a['read_time']}</span>
          </div>
        </a>""")
    grid = "\n\n".join(cards)
    index_path = os.path.join(BLOG, "index.html")
    with open(index_path, encoding="utf-8") as f:
        content = f.read()
    content = re.sub(
        r'<div class="blog-grid">.*?</div>\s*</div>\s*</section>',
        f'<div class="blog-grid">\n{grid}\n      </div>\n    </div>\n  </section>',
        content,
        flags=re.DOTALL,
    )
    content = content.replace(NAV_INDEX_OLD, NAV_INDEX_NEW)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    os.makedirs(ASSETS, exist_ok=True)

    for filename, config in SVG_CONFIGS.items():
        path = os.path.join(ASSETS, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_architecture_svg(config))
        print(f"SVG: {path}")

    for slug, info in CLOUD_ARTICLES.items():
        meta = next(a for a in ARTICLES if a["slug"] == slug)
        out_dir = os.path.join(BLOG, slug)
        os.makedirs(out_dir, exist_ok=True)
        html = article_html(meta, info)
        if "\u2014" in html:
            raise ValueError(f"Em dash in {slug}")
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Article: {slug}")

    update_article_dates()
    regenerate_blog_index()
    print("Done: dates, nav, and blog index updated.")


if __name__ == "__main__":
    main()
