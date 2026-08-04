#!/usr/bin/env python3
"""Generate blog post HTML files from article definitions."""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")

NAV = """  <nav class="nav" id="nav">
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
        <li><a href="../index.html#contact" class="nav__cta">Contact</a></li>
      </ul>
    </div>
  </nav>"""


def html_page(article):
    tags_html = "\n".join(
        f'            <span class="blog-tag">{t}</span>' for t in article["tags"]
    )
    body = "\n".join(article["body"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{article['description']}">
  <meta name="author" content="Antony Britto C J">
  <title>{article['title']} | Antony Britto C J</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../styles.css">
  <link rel="stylesheet" href="../post.css">
  <link rel="icon" type="image/png" href="../../assets/favicon.png">
</head>
<body>
{NAV}

  <section class="blog-post">
    <div class="container">
      <article class="blog-content">
        <div class="blog-header">
          <h1 class="blog-title">{article['title']}</h1>
          <div class="blog-meta">
            <div class="blog-meta-item">📅 {article['date']}</div>
            <div class="blog-meta-item">⏱️ {article['read_time']} read</div>
          </div>
        </div>

        <p class="blog-lead">{article['lead']}</p>

{body}

        <div class="blog-tags">
          <div class="blog-tags-title">Topics &amp; Tags</div>
          <div class="blog-tags-list">
{tags_html}
          </div>
        </div>

        <div class="blog-nav">
          <a href="../index.html">← Back to All Posts</a>
        </div>
      </article>
    </div>
  </section>

  <script src="../../script.js"></script>
</body>
</html>
"""


def p(text):
    return f"        <p>{text}</p>"


def h2(text):
    return f"        <h2>{text}</h2>"


def ul(items):
    lines = ["        <ul>"]
    for item in items:
        lines.append(f"          <li>{item}</li>")
    lines.append("        </ul>")
    return "\n".join(lines)


ARTICLES = [
    {
        "slug": "multi-cloud-strategies",
        "title": "Designing Multi-Cloud Strategies for Enterprise Scale",
        "description": "Best practices for building resilient, cost-effective multi-cloud architectures across AWS, Azure, GCP, and OCI.",
        "date": "July 15, 2026",
        "read_time": "5 min",
        "lead": "Best practices for building resilient, cost-effective multi-cloud architectures across AWS, Azure, GCP, and OCI.",
        "tags": ["Multi-Cloud", "AWS", "Azure", "GCP", "OCI", "Cloud Architecture"],
        "body": [
            p("Multi-cloud is rarely a goal in itself. It is a response to acquisition history, regulatory requirements, vendor negotiations, or the need to place workloads where they perform best. After architecting solutions across AWS, Azure, GCP, and OCI for enterprise clients, the pattern is consistent: success depends less on how many clouds you use and more on how deliberately you govern them."),
            h2("Start With Workload Placement, Not Provider Preference"),
            p("Map each workload to a cloud based on capability fit, data residency, existing team skills, and commercial terms. A marketplace platform might span four providers for customer choice, while a regulated workload might stay on a single cloud with strict controls. Document the rationale so future teams do not reverse good decisions without understanding why they were made."),
            h2("Build a Consistent Abstraction Layer"),
            p("Without shared standards, every cloud becomes a snowflake. Standardize on Terraform modules, container images, CI/CD patterns, and observability stacks that work across providers. Kubernetes often serves as the compute abstraction. For networking, accept that VPC designs differ and invest in clear connectivity patterns: hub-and-spoke, cloud exchange, or dedicated interconnects."),
            h2("Governance and Cost Control at Scale"),
            p("Centralize identity federation, tagging policies, and security baselines. FinOps across multiple clouds requires a single cost view and accountability model. Teams that migrated 200+ servers with minimal downtime did so by treating migration waves as products: defined scope, rollback plans, and measurable success criteria."),
            p("Multi-cloud done well gives you optionality without chaos. Done poorly, it multiplies operational burden by the number of providers you adopt."),
        ],
    },
    {
        "slug": "gitops-declarative-infrastructure",
        "title": "GitOps: Declarative Infrastructure for Modern Teams",
        "description": "How GitOps principles enable consistent, auditable, and automated infrastructure deployments at scale.",
        "date": "July 12, 2026",
        "read_time": "5 min",
        "lead": "How GitOps principles enable consistent, auditable, and automated infrastructure deployments at scale.",
        "tags": ["GitOps", "Kubernetes", "ArgoCD", "Flux", "CI/CD", "DevOps"],
        "body": [
            p("GitOps extends the idea that Git is the single source of truth from application code to infrastructure and cluster state. When you declare desired state in version control and let a controller reconcile reality against it, you gain auditability, rollback capability, and a workflow developers already understand."),
            h2("The Core Loop"),
            p("Define infrastructure and application manifests in Git. A CI pipeline validates and merges changes. A GitOps operator (Argo CD, Flux, or similar) continuously compares the live cluster against the declared state and applies diffs. Drift is visible and correctable. Every production change has an author, a reviewer, and a commit hash."),
            h2("What Belongs in Git"),
            p("Kubernetes manifests, Helm values, Kustomize overlays, Terraform modules consumed by pipelines, and policy definitions all fit naturally. Keep secrets out of plain Git: use sealed secrets, external secret operators, or vault integrations. Structure repositories by environment or by application, but be consistent so on-call engineers know where to look at 2 AM."),
            h2("Practical Lessons From the Field"),
            p("Start with one non-critical workload. Prove the promotion path from dev to staging to production. Add progressive delivery and automated sync only after the basics work. GitOps pairs well with platform engineering: golden paths become Git templates that teams fork and customize within guardrails."),
            p("The goal is not more YAML. The goal is predictable, reviewable change at the speed your business requires."),
        ],
    },
    {
        "slug": "kubernetes-networking-cni",
        "title": "Kubernetes Networking: Understanding CNI Plugins",
        "description": "Deep dive into Container Networking Interface, overlay networks, and service mesh considerations.",
        "date": "July 10, 2026",
        "read_time": "5 min",
        "lead": "Deep dive into Container Networking Interface, overlay networks, and service mesh considerations.",
        "tags": ["Kubernetes", "CNI", "Networking", "Calico", "Cilium", "Service Mesh"],
        "body": [
            p("Kubernetes networking confuses many teams because pods get IPs, services get virtual IPs, and nodes have their own interfaces. The Container Networking Interface (CNI) is the plugin layer that makes pod-to-pod communication possible on every node."),
            h2("How CNI Fits Together"),
            p("When the kubelet starts a pod, it calls the configured CNI plugin. The plugin assigns an IP, sets up routes, and may apply network policies. Common choices include Calico for policy-rich flat networking, Cilium for eBPF-powered observability and security, and Flannel for simpler overlay setups. Your choice affects performance, policy expressiveness, and operational complexity."),
            h2("Services, Ingress, and Beyond"),
            p("ClusterIP services provide stable endpoints inside the cluster. Ingress or Gateway API resources expose HTTP routes to the outside world. For east-west traffic encryption, mutual TLS, and fine-grained retries, a service mesh (Istio, Linkerd) adds a data plane proxy. Not every cluster needs a mesh on day one. Start with solid CNI and ingress, then add mesh when cross-service security or traffic management justifies the overhead."),
            h2("Debugging Network Issues"),
            p("When a pod cannot reach a service, work through DNS resolution, network policies, security groups, and CNI health in that order. Tools like <code>kubectl exec</code>, <code>nslookup</code>, and <code>ss -tlnp</code> inside the pod narrow the failure domain quickly."),
            p("Understanding CNI is what separates teams that fight Kubernetes networking from teams that operate it confidently."),
        ],
    },
    {
        "slug": "scalable-ml-pipelines",
        "title": "Building Scalable ML Pipelines with Cloud Infrastructure",
        "description": "Architecture patterns for ML workflows, data processing, and model serving in cloud-native environments.",
        "date": "July 8, 2026",
        "read_time": "4 min",
        "lead": "Architecture patterns for ML workflows, data processing, and model serving in cloud-native environments.",
        "tags": ["MLOps", "Machine Learning", "Cloud", "Kubernetes", "Data Pipelines"],
        "body": [
            p("Machine learning in production is an engineering problem dressed in statistics. Models need versioned data, reproducible training, validated artifacts, and serving infrastructure that scales with demand. Cloud-native patterns make this tractable."),
            h2("Pipeline Stages"),
            p("Ingest raw data into object storage or a data lake. Transform and feature-engineer in batch or stream jobs. Train models on GPU-enabled compute, whether managed services or Kubernetes jobs. Register model versions in a model registry. Deploy behind an API or batch inference queue. Monitor for drift, latency, and data quality regressions."),
            h2("Platform Choices"),
            p("Managed ML platforms accelerate time to value. Kubernetes with Kubeflow or custom operators gives control for teams with platform engineering capacity. RAG and agentic workloads add vector databases and orchestration layers (LangChain, custom pipelines) on top of the same foundation."),
            h2("What Enterprise Teams Get Wrong"),
            p("Treating notebooks as production code. Skipping data versioning. Deploying models without rollback paths. Build the same discipline you apply to application releases: CI/CD, testing, and observability from the start."),
            p("Scalable ML is less about the algorithm and more about the platform around it."),
        ],
    },
    {
        "slug": "zero-trust-architecture",
        "title": "Zero Trust Architecture in Cloud Environments",
        "description": "Implementing zero-trust principles for identity, access control, and network security at enterprise scale.",
        "date": "July 5, 2026",
        "read_time": "4 min",
        "lead": "Implementing zero-trust principles for identity, access control, and network security at enterprise scale.",
        "tags": ["Zero Trust", "Security", "IAM", "DevSecOps", "Cloud Security"],
        "body": [
            p("Zero trust replaces the assumption that internal networks are safe. Every request is authenticated, authorized, and encrypted regardless of origin. In cloud environments where perimeters are fluid, this is not optional."),
            h2("Identity as the Perimeter"),
            p("Strong identity federation across clouds, short-lived credentials, and role-based access with least privilege. Service accounts need the same rigor as human users. Tools like IAM policies, workload identity, and secrets managers enforce boundaries programmatically."),
            h2("Network Micro-Segmentation"),
            p("Security groups, network policies, and private endpoints limit blast radius. East-west traffic between services should be explicitly allowed, not implicitly trusted. For hybrid setups, connect on-premises and cloud with encrypted tunnels and consistent policy."),
            h2("Continuous Verification"),
            p("Integrate vulnerability scanning, policy-as-code checks, and runtime threat detection into CI/CD. DevSecOps is zero trust applied to the delivery pipeline. Security reviews become automated gates rather than end-of-project checklists."),
            p("Zero trust is a journey of smaller perimeters and stronger identity, not a single product purchase."),
        ],
    },
    {
        "slug": "building-internal-developer-platforms",
        "title": "Building Internal Developer Platforms (IDP)",
        "description": "Creating self-service infrastructure and standardized deployment platforms that empower development teams.",
        "date": "July 3, 2026",
        "read_time": "5 min",
        "lead": "Creating self-service infrastructure and standardized deployment platforms that empower development teams.",
        "tags": ["Platform Engineering", "IDP", "Developer Experience", "Kubernetes", "Self-Service"],
        "body": [
            p("Platform engineering exists because every product team should not rebuild Kubernetes, CI/CD, and observability from scratch. An Internal Developer Platform (IDP) packages approved patterns into self-service workflows that feel like a product, not a ticket queue."),
            h2("What a Good IDP Provides"),
            p("Golden paths for deploying services: scaffold a repo, provision namespaces, wire CI/CD, and expose dashboards in minutes. Backstage, custom portals, or Git-based templates all work. The interface matters less than consistency and clear ownership."),
            h2("Build vs. Buy vs. Compose"),
            p("Most enterprises compose: managed Kubernetes, Terraform modules, Argo CD, Prometheus, and a portal layer. Platform teams curate the catalog, enforce guardrails, and measure adoption. Developers stay in flow; operators retain control."),
            h2("Measuring Success"),
            p("Track lead time for changes, deployment frequency, and developer satisfaction. If teams bypass the platform, listen to why. Friction is feedback. The best IDPs evolve with the teams they serve."),
            p("A platform is successful when developers choose it because it is the fastest path to production, not because policy forces them."),
        ],
    },
    {
        "slug": "observability-vs-monitoring",
        "title": "Observability vs. Monitoring: Why the Distinction Matters",
        "description": "Understanding logs, metrics, traces, and how to build truly observable systems.",
        "date": "June 30, 2026",
        "read_time": "5 min",
        "lead": "Understanding logs, metrics, traces, and how to build truly observable systems.",
        "tags": ["Observability", "Monitoring", "Prometheus", "Grafana", "OpenTelemetry", "SRE"],
        "body": [
            p("Monitoring tells you when something you predicted might break has broken. Observability lets you ask new questions about systems you did not anticipate failing. Both matter. Confusing them leads to alert fatigue without diagnostic depth."),
            h2("The Three Pillars"),
            p("<strong>Metrics</strong> are aggregated numbers over time: CPU, request rate, error ratio. <strong>Logs</strong> are discrete events with context. <strong>Traces</strong> follow a request across services. Together they answer: what is broken, where, and why."),
            h2("Building Observable Systems"),
            p("Instrument at boundaries: HTTP handlers, database calls, queue consumers. Use OpenTelemetry for vendor-neutral collection. Standardize on Prometheus and Grafana or your cloud provider's managed stack, but keep export paths open."),
            h2("SRE Practices That Stick"),
            p("Define SLIs and SLOs tied to user experience. Alert on symptoms, not every internal metric. Runbooks linked from alerts reduce mean time to recovery. Blameless postmortems turn incidents into durable improvements."),
            p("Observability is an investment in unknown unknowns. Monitoring is the safety net for known risks. You need both."),
        ],
    },
    {
        "slug": "cloud-cost-optimization",
        "title": "Cloud Cost Optimization: Beyond Just Shutting Down Resources",
        "description": "Strategic approaches to FinOps, reserved instances, and building cost-conscious cloud cultures.",
        "date": "June 27, 2026",
        "read_time": "5 min",
        "lead": "Strategic approaches to FinOps, reserved instances, and building cost-conscious cloud cultures.",
        "tags": ["FinOps", "Cost Optimization", "Cloud Governance", "AWS", "Azure"],
        "body": [
            p("Turning off idle instances is table stakes. Sustained 40 to 60 percent cost reduction, which I have delivered across enterprise migrations, comes from architecture, governance, and culture working together."),
            h2("Right-Sizing and Commitment Strategies"),
            p("Analyze utilization before resizing. Reserved instances and savings plans reward predictable workloads. Spot and preemptible instances suit fault-tolerant batch jobs. Autoscaling prevents paying for peak capacity around the clock."),
            h2("Architectural Cost Levers"),
            p("Serverless and containers reduce waste when workloads are bursty. Data transfer between regions and clouds is a silent budget killer. Design data gravity intentionally. Cache aggressively. Lifecycle policies on object storage tier cold data automatically."),
            h2("FinOps as a Practice"),
            p("Tag everything. Assign cost centers. Review spend monthly with engineering leads, not only finance. Make cost visible in CI/CD: estimate Terraform plan costs before merge. Teams optimize what they can see."),
            p("Cost optimization is continuous engineering, not a one-time cleanup project."),
        ],
    },
    {
        "slug": "rto-rpo-business-continuity",
        "title": "RTO and RPO: Planning for Business Continuity",
        "description": "Designing resilient architectures with recovery time and recovery point objectives in mind.",
        "date": "June 25, 2026",
        "read_time": "4 min",
        "lead": "Designing resilient architectures with recovery time and recovery point objectives in mind.",
        "tags": ["Disaster Recovery", "RTO", "RPO", "Business Continuity", "Resilience"],
        "body": [
            p("Recovery Time Objective (RTO) is how long you can be down. Recovery Point Objective (RPO) is how much data you can afford to lose. Every architecture decision should trace back to these numbers, agreed with the business, not invented by engineering."),
            h2("Matching Architecture to Objectives"),
            p("RPO of minutes requires synchronous replication or frequent backups. RTO of hours allows warm standby. RTO of days might rely on cold backups and runbooks. Not every system needs the same tier. Classify workloads and spend resilience budget where it matters."),
            h2("Testing Recovery"),
            p("Untested backups are wishful thinking. Schedule game days. Fail over to secondary regions. Measure actual RTO and RPO against targets. Document gaps and fund fixes."),
            h2("Cloud-Native DR Patterns"),
            p("Multi-AZ for availability within a region. Cross-region replication for regional disasters. Infrastructure as Code makes rebuilding environments repeatable. GitOps ensures configuration state is recoverable from version control."),
            p("Resilience is a business contract expressed in minutes and megabytes, then engineered to match."),
        ],
    },
    {
        "slug": "serverless-when-to-use",
        "title": "Serverless Computing: When and When Not to Use It",
        "description": "Evaluating serverless vs. containers, cold start challenges, and cost implications.",
        "date": "June 22, 2026",
        "read_time": "4 min",
        "lead": "Evaluating serverless vs. containers, cold start challenges, and cost implications.",
        "tags": ["Serverless", "Lambda", "Cloud Functions", "Containers", "Architecture"],
        "body": [
            p("Serverless removes server management and scales to zero. It is excellent for event-driven workloads, APIs with variable traffic, and glue logic between services. It is a poor default for steady high-throughput systems or workloads with strict latency requirements at cold start."),
            h2("When Serverless Wins"),
            p("Infrequent jobs, webhooks, file processing triggers, and prototype APIs. Pay per invocation aligns cost with usage. Managed scaling handles traffic spikes without capacity planning."),
            h2("When Containers Win"),
            p("Long-running processes, custom runtimes, predictable baseline load, and teams already standardized on Kubernetes. Containers offer more control over networking, filesystem, and dependencies."),
            h2("Hybrid Approaches"),
            p("Many enterprises use both: Kubernetes for core services, functions for event handling. Watch data egress costs and vendor lock-in on proprietary event sources. Abstract critical logic behind interfaces you own."),
            p("Choose serverless for operational simplicity at the right scale, not because it is fashionable."),
        ],
    },
    {
        "slug": "edge-computing-sovereign-infrastructure",
        "title": "Edge Computing and the Future of Sovereign Infrastructure",
        "description": "Distributed computing at the edge, data residency, and building sovereign cloud appliances.",
        "date": "June 20, 2026",
        "read_time": "5 min",
        "lead": "Distributed computing at the edge, data residency, and building sovereign cloud appliances.",
        "tags": ["Edge Computing", "Sovereign Cloud", "Data Residency", "Hybrid Cloud"],
        "body": [
            p("Edge computing moves compute closer to data sources and users. Sovereign infrastructure ensures data and control stay within jurisdictional boundaries. Together they address latency, compliance, and national digital autonomy."),
            h2("Why Edge Matters"),
            p("Manufacturing, healthcare, and telecom generate data at the source. Sending everything to a central cloud adds latency and bandwidth cost. Edge nodes run filtering, inference, and aggregation locally, syncing summaries upstream."),
            h2("Sovereign Cloud Appliances"),
            p("Designing sovereign edge appliances means packaging Kubernetes, storage, and security controls into deployable units that operate disconnected or semi-connected. Full data residency, auditable supply chains, and operator-controlled updates are non-negotiable."),
            h2("Operational Reality"),
            p("Remote sites lack 24/7 staff. GitOps, centralized monitoring with local buffering, and automated remediation are essential. Treat each edge node as a small datacenter with the same discipline as your core cloud."),
            p("The future is distributed, regulated, and still cloud-native in how it is operated."),
        ],
    },
    {
        "slug": "sql-vs-nosql",
        "title": "SQL vs. NoSQL: Choosing the Right Database for Your Use Case",
        "description": "Evaluation criteria for relational databases, document stores, time-series, and graph databases.",
        "date": "June 18, 2026",
        "read_time": "3 min",
        "lead": "Evaluation criteria for relational databases, document stores, time-series, and graph databases.",
        "tags": ["Database", "PostgreSQL", "MongoDB", "SQL", "NoSQL"],
        "body": [
            p("The SQL vs. NoSQL debate is outdated. Modern architects pick the data store that fits access patterns, consistency needs, and operational capacity."),
            h2("When SQL Fits"),
            p("Transactional workloads, complex joins, strong consistency, and mature reporting. PostgreSQL handles JSON well, blurring the line. Use relational databases when integrity and ACID matter."),
            h2("When NoSQL Fits"),
            p("Document stores for flexible schemas. Key-value for session caches. Time-series databases for metrics. Graph databases for relationship-heavy queries. DynamoDB and MongoDB scale horizontally when designed for their access patterns."),
            h2("Decision Framework"),
            ul([
                "What are the read and write patterns?",
                "How much consistency does the business require?",
                "Can the team operate and backup this technology?",
                "Will requirements change enough to need schema flexibility?",
            ]),
            p("Polyglot persistence is normal. One database per service, chosen deliberately, beats one size fits all."),
        ],
    },
    {
        "slug": "monolith-to-microservices",
        "title": "From Monolith to Microservices: A Pragmatic Migration Strategy",
        "description": "Planning and executing microservices adoption without the operational chaos.",
        "date": "June 15, 2026",
        "read_time": "4 min",
        "lead": "Planning and executing microservices adoption without the operational chaos.",
        "tags": ["Microservices", "Architecture", "Migration", "Kubernetes"],
        "body": [
            p("Microservices solve organizational scaling problems as much as technical ones. Splitting a monolith without clear boundaries creates distributed monoliths: all the pain, none of the simplicity."),
            h2("Strangler Fig Pattern"),
            p("Route traffic incrementally from the monolith to new services. Start at seams that are already loosely coupled. Keep the monolith running while extracting high-change domains first."),
            h2("Prerequisites Before You Split"),
            p("CI/CD maturity, observability, and deployment automation. If you cannot deploy the monolith reliably, microservices will not help. Define service ownership and API contracts before writing code."),
            h2("Avoid Common Traps"),
            p("Too many services too soon. Shared databases between services. Synchronous chains that amplify failures. Invest in platform capabilities (service mesh, API gateway, standard libraries) as you grow."),
            p("A pragmatic migration respects that the monolith paid for your success. Evolve it, do not declare war on it."),
        ],
    },
    {
        "slug": "api-governance-at-scale",
        "title": "API Governance and Management at Scale",
        "description": "Implementing API standards, versioning strategies, and developer experience considerations.",
        "date": "June 12, 2026",
        "read_time": "3 min",
        "lead": "Implementing API standards, versioning strategies, and developer experience considerations.",
        "tags": ["API Management", "REST", "Governance", "Developer Experience"],
        "body": [
            p("APIs are contracts between teams. Without governance, every service invents its own conventions and integration becomes expensive."),
            h2("Standards That Matter"),
            p("Consistent naming, error formats, pagination, and authentication. OpenAPI specifications as the source of truth. Version in URLs or headers, but pick one approach and document deprecation timelines."),
            h2("Developer Experience"),
            p("Sandbox environments, interactive documentation, and SDKs where justified. Rate limiting and quotas protect backends. Analytics show which APIs deliver value and which linger unused."),
            h2("Governance Without Bureaucracy"),
            p("Lightweight design reviews for external-facing APIs. Automated linting of OpenAPI specs in CI. A central catalog (Backstage or dedicated portal) for discovery."),
            p("Good API governance accelerates teams. Bad governance sends them around the platform."),
        ],
    },
    {
        "slug": "devops-culture-beyond-tools",
        "title": "Building a DevOps Culture: Beyond Tools and Automation",
        "description": "Organizational change, breaking silos, and fostering shared responsibility for production.",
        "date": "June 10, 2026",
        "read_time": "5 min",
        "lead": "Organizational change, breaking silos, and fostering shared responsibility for production.",
        "tags": ["DevOps Culture", "Collaboration", "SRE", "Leadership"],
        "body": [
            p("DevOps is not a toolchain. It is shared ownership of outcomes from commit to customer. Tools enable culture; they do not replace it."),
            h2("Breaking Down Silos"),
            p("Developers who deploy. Operators who contribute to application design. Security embedded early, not at the end. Cross-functional teams aligned to products, not functions."),
            h2("Psychological Safety"),
            p("Blameless postmortems. Incidents are learning opportunities. Leaders who reward transparency about failures build teams that fix problems faster."),
            h2("Metrics That Reinforce Culture"),
            p("Measure lead time, deployment frequency, change failure rate, and recovery time. Celebrate improvements. Avoid vanity metrics that encourage hiding problems."),
            p("After 26 years in IT, the teams that succeed are the ones that trust each other under pressure. Automation follows from that trust."),
        ],
    },
    {
        "slug": "iac-best-practices",
        "title": "IaC Best Practices: Terraform, CloudFormation, and Beyond",
        "description": "State management, modularity, testing, and GitOps integration for infrastructure code.",
        "date": "June 7, 2026",
        "read_time": "5 min",
        "lead": "State management, modularity, testing, and GitOps integration for infrastructure code.",
        "tags": ["Terraform", "CloudFormation", "IaC", "GitOps", "Ansible"],
        "body": [
            p("Infrastructure as Code turns environments into reviewable, repeatable artifacts. Terraform, CloudFormation, Bicep, and Ansible each have strengths. Consistency in how you use them matters more than which you pick."),
            h2("Modularity and Reuse"),
            p("Compose small modules with clear inputs and outputs. Pin provider versions. Document assumptions. A module library is how platform teams scale governance without becoming a bottleneck."),
            h2("State and Drift"),
            p("Remote state with locking prevents corruption. Regular drift detection reconciles manual console changes. Treat state files as sensitive assets."),
            h2("Testing and CI"),
            p("Validate, plan, and policy-check on every pull request. Tools like Checkov, tfsec, and OPA catch misconfigurations early. Promote through environments with the same pipeline discipline as application code."),
            p("IaC is how you make infrastructure changes boring in the best possible way."),
        ],
    },
    {
        "slug": "on-call-excellence",
        "title": "On-Call Excellence: Building Effective Incident Response",
        "description": "Runbooks, blameless postmortems, and creating sustainable on-call rotations.",
        "date": "June 5, 2026",
        "read_time": "4 min",
        "lead": "Runbooks, blameless postmortems, and creating sustainable on-call rotations.",
        "tags": ["On-Call", "Incident Management", "SRE", "Runbooks"],
        "body": [
            p("On-call should be rare, actionable, and survivable. If your team dreads the rotation, fix the system before you fix the people."),
            h2("Runbooks and Alert Quality"),
            p("Every alert links to a runbook with diagnostic steps and escalation paths. Alert on user-impacting symptoms. Tune noisy alerts aggressively. Pages should mean action required now."),
            h2("Incident Response"),
            p("Designate roles: incident commander, communications, technical lead. Use a shared channel and timeline. Resolve first, analyze second. Document decisions as you go."),
            h2("Sustainable Rotations"),
            p("Limit shift length. Compensate fairly. Follow the sun for global teams. Track toil and fund automation from postmortem action items. Burned-out on-call engineers leave; resilient systems retain them."),
            p("Excellent on-call is a product of observable systems and honest postmortems."),
        ],
    },
    {
        "slug": "testing-infrastructure",
        "title": "Testing Infrastructure: Unit, Integration, and End-to-End Tests",
        "description": "Building test pyramids, chaos engineering, and ensuring infrastructure reliability.",
        "date": "June 2, 2026",
        "read_time": "4 min",
        "lead": "Building test pyramids, chaos engineering, and ensuring infrastructure reliability.",
        "tags": ["Testing", "Infrastructure", "Chaos Engineering", "CI/CD"],
        "body": [
            p("Infrastructure code deserves the same test discipline as application code. Untested Terraform is production roulette."),
            h2("Layers of Testing"),
            p("<strong>Static analysis</strong> catches syntax and policy violations. <strong>Unit tests</strong> validate module logic with mock providers. <strong>Integration tests</strong> spin ephemeral environments. <strong>End-to-end tests</strong> verify critical paths in staging before promotion."),
            h2("Chaos Engineering"),
            p("Deliberately inject failures: kill nodes, throttle networks, expire certificates. Game days prove your assumptions about resilience. Start in non-production, graduate to controlled production experiments."),
            h2("CI Integration"),
            p("Plan on PR, apply on merge to dev, promote with gates. Cost estimation and policy checks are tests too. Failed pipelines block releases."),
            p("Reliable infrastructure is tested infrastructure."),
        ],
    },
    {
        "slug": "compliance-as-code",
        "title": "Compliance as Code: Automating Governance and Audits",
        "description": "Policy as Code, automated compliance checks, and maintaining audit trails.",
        "date": "May 30, 2026",
        "read_time": "3 min",
        "lead": "Policy as Code, automated compliance checks, and maintaining audit trails.",
        "tags": ["Compliance", "Policy as Code", "Governance", "Security"],
        "body": [
            p("Manual compliance audits do not scale with cloud velocity. Policy as Code encodes requirements into automated checks that run continuously."),
            h2("Tools and Patterns"),
            p("OPA/Rego, Sentinel, and cloud-native config rules evaluate Terraform plans and live resources. Fail builds that violate encryption, tagging, or network exposure policies."),
            h2("Audit Trails"),
            p("Git history for infrastructure changes. Immutable logs for access and deployments. Evidence collection becomes a byproduct of normal workflows, not a quarterly scramble."),
            p("Compliance as code turns audits from events into continuous assurance."),
        ],
    },
    {
        "slug": "performance-optimization",
        "title": "Performance Optimization: From Application to Infrastructure",
        "description": "Profiling, bottleneck identification, and scaling strategies at each layer.",
        "date": "May 27, 2026",
        "read_time": "4 min",
        "lead": "Profiling, bottleneck identification, and scaling strategies at each layer.",
        "tags": ["Performance", "Optimization", "Scaling", "Observability"],
        "body": [
            p("Performance work starts with measurement, not assumptions. Profile before you scale. Scaling hides inefficiency until the bill arrives."),
            h2("Application Layer"),
            p("Identify slow queries, N+1 patterns, and blocking I/O. Cache at the right tier. Async processing for non-critical paths."),
            h2("Infrastructure Layer"),
            p("Right-size compute. Use CDN for static assets. Connection pooling and keep-alive for databases. Autoscale on meaningful metrics, not CPU alone."),
            h2("Systematic Approach"),
            p("Define SLOs. Load test before launch. Compare before and after every change. Document bottlenecks and revisit as traffic grows."),
            p("Fast systems are designed, measured, and iterated, not guessed."),
        ],
    },
    {
        "slug": "cloud-networking-vpcs",
        "title": "Understanding Cloud Networking: VPCs, Subnets, and Routing",
        "description": "Network architecture patterns, VPC design, and connectivity between cloud and on-premises.",
        "date": "May 25, 2026",
        "read_time": "5 min",
        "lead": "Network architecture patterns, VPC design, and connectivity between cloud and on-premises.",
        "tags": ["Networking", "VPC", "Hybrid Cloud", "AWS", "Azure"],
        "body": [
            p("Cloud networking is software-defined but the fundamentals persist: IP addressing, routing, firewalls, and DNS. VPCs are your private network boundaries in the cloud."),
            h2("VPC Design Principles"),
            p("Segment by environment and tier: public subnets for load balancers, private subnets for applications and data. Avoid overlapping CIDR blocks across VPCs and on-premises networks. Plan for growth."),
            h2("Connectivity Patterns"),
            p("VPN for quick hybrid links. Dedicated interconnect for production throughput. Transit gateways and hub-spoke topologies simplify multi-VPC routing. DNS resolution across boundaries needs explicit design."),
            h2("Security Layers"),
            p("Security groups are stateful firewalls at the instance level. NACLs for subnet boundaries. Private endpoints keep traffic off the public internet. Network policies in Kubernetes add another layer for pods."),
            p("Solid VPC design prevents the networking surprises that derail migrations and scale-out efforts."),
        ],
    },
    {
        "slug": "data-pipelines-etl",
        "title": "Data Pipelines and ETL: Modern Approaches",
        "description": "Stream processing, batch processing, data warehousing, and real-time analytics.",
        "date": "May 22, 2026",
        "read_time": "3 min",
        "lead": "Stream processing, batch processing, data warehousing, and real-time analytics.",
        "tags": ["Data Engineering", "ETL", "Kafka", "Analytics"],
        "body": [
            p("Modern data pipelines blend batch and stream processing. ETL became ELT: load raw data first, transform in the warehouse where compute scales elastically."),
            h2("Batch vs. Stream"),
            p("Batch suits reports, billing, and historical analysis. Streams power real-time dashboards, fraud detection, and event-driven applications. Kafka is the common backbone; managed services reduce operational load."),
            h2("Warehouse and Lakehouse"),
            p("Centralize analytics data with clear lineage. Schema evolution and data quality checks belong in the pipeline, not as afterthoughts."),
            p("Choose pipeline architecture based on latency requirements and who consumes the data."),
        ],
    },
    {
        "slug": "contributing-open-source",
        "title": "Contributing to Open Source: A Guide for Cloud Engineers",
        "description": "Finding the right projects, making meaningful contributions, and building community.",
        "date": "May 20, 2026",
        "read_time": "3 min",
        "lead": "Finding the right projects, making meaningful contributions, and building community.",
        "tags": ["Open Source", "Community", "Career", "Kubernetes"],
        "body": [
            p("Open source is how cloud-native tooling evolves. Contributing builds skills, reputation, and network faster than passive learning."),
            h2("Where to Start"),
            p("Use tools you already run: Terraform providers, CNCF projects, CLI utilities. Fix documentation typos. Triage issues. Small, merged PRs build trust."),
            h2("Meaningful Contributions"),
            p("Reproduce bugs with clear reports. Reference issues in commits. Follow project conventions. Be patient with maintainers who volunteer their time."),
            p("The best contributors solve problems they have personally encountered in production."),
        ],
    },
    {
        "slug": "mlops-operationalizing-models",
        "title": "MLOps: Operationalizing Machine Learning Models",
        "description": "Model training, validation, deployment, monitoring, and continuous improvement cycles.",
        "date": "May 17, 2026",
        "read_time": "4 min",
        "lead": "Model training, validation, deployment, monitoring, and continuous improvement cycles.",
        "tags": ["MLOps", "Machine Learning", "AI", "DevOps"],
        "body": [
            p("A model in a notebook is not a product. MLOps applies DevOps discipline to the ML lifecycle: data, training, deployment, and monitoring."),
            h2("The ML Lifecycle"),
            p("Version datasets and features. Automate training pipelines. Validate with holdout sets and business metrics, not accuracy alone. Deploy with canaries and rollback. Monitor drift and retrain on schedule or trigger."),
            h2("Platform Integration"),
            p("RAG pipelines and conversational AI add retrieval, prompt management, and evaluation layers. Treat prompts and embeddings as versioned artifacts alongside model weights."),
            p("MLOps closes the gap between experimentation and reliable AI in production."),
        ],
    },
    {
        "slug": "growing-cloud-career",
        "title": "Growing Your Cloud Engineering Career: Skills and Mindset",
        "description": "Continuous learning, certifications, building a strong professional network, and thought leadership.",
        "date": "May 15, 2026",
        "read_time": "3 min",
        "lead": "Continuous learning, certifications, building a strong professional network, and thought leadership.",
        "tags": ["Career", "Cloud Engineering", "Certifications", "Learning"],
        "body": [
            p("Cloud engineering rewards breadth and depth. After 12+ years in cloud and 26 in IT, the constant is learning speed, not any single technology."),
            h2("Skills That Compound"),
            p("Linux fundamentals, networking, and security underpin every cloud role. IaC, containers, and CI/CD are table stakes. Communication and architecture thinking differentiate seniors from implementers."),
            h2("Certifications and Proof"),
            p("Certs open doors; projects keep them open. Build something: migrate a workload, publish a runbook, contribute to open source. Document what you learned."),
            h2("Network and Visibility"),
            p("Share knowledge through writing and speaking. Mentor juniors. The best opportunities often come from reputation built over years, not job boards."),
            p("Careers are marathons. Invest in fundamentals that survive every hype cycle."),
        ],
    },
    {
        "slug": "technology-trends-2026",
        "title": "Technology Trends 2026: What's Shaping the Cloud Landscape",
        "description": "AI integration, quantum computing, edge computing, and emerging architectural patterns.",
        "date": "May 12, 2026",
        "read_time": "4 min",
        "lead": "AI integration, quantum computing, edge computing, and emerging architectural patterns.",
        "tags": ["Innovation", "AI", "Edge Computing", "Cloud Trends"],
        "body": [
            p("2026 is defined by AI moving from experiments to production platforms, edge infrastructure maturing, and cost discipline returning after years of growth-at-all-costs spending."),
            h2("Agentic AI and Platforms"),
            p("AI agents that plan, use tools, and execute workflows require new platform capabilities: guardrails, observability, cost controls, and human oversight. RAG remains the bridge between enterprise data and models."),
            h2("Sovereign and Edge Infrastructure"),
            p("Data residency drives regional clouds and sovereign appliances. Edge nodes run inference locally. Hybrid patterns connect them to central governance."),
            h2("Platform Engineering Matures"),
            p("IDPs, GitOps, and FinOps are standard practice, not differentiators. Teams that compose these well ship faster than teams chasing the next tool."),
            p("Trends matter when they change how you design systems. Adopt deliberately."),
        ],
    },
    {
        "slug": "leading-technical-teams",
        "title": "Leading Technical Teams: From IC to Manager",
        "description": "Transitioning roles, mentoring, delegation, and building high-performing teams.",
        "date": "May 10, 2026",
        "read_time": "5 min",
        "lead": "Transitioning roles, mentoring, delegation, and building high-performing teams.",
        "tags": ["Leadership", "Management", "Mentoring", "Teams"],
        "body": [
            p("Moving from individual contributor to technical leader changes your output from code to multiplied team capability. Leading teams of 5 to 8 engineers taught me that clarity and trust matter more than technical heroics."),
            h2("Delegation Without Abdication"),
            p("Assign ownership with context, not just tasks. Review outcomes, not every line. Stay technical enough to spot risks, but let the team solve problems."),
            h2("Mentoring and Growth"),
            p("Regular one-on-ones. Career conversations beyond the next sprint. Code reviews as teaching moments. Celebrate public wins; address issues privately."),
            h2("Architecture Governance"),
            p("Set standards, document decisions (ADRs), and involve the team in shaping them. Presales and client-facing work require translating complexity into business value, a skill that separates architects from operators."),
            p("The best technical leaders make everyone around them better. That is the job."),
        ],
    },
    {
        "slug": "green-cloud-sustainable-computing",
        "title": "Green Cloud: Sustainable Computing and Carbon-Aware Architectures",
        "description": "Building environmentally responsible infrastructure, energy-efficient operations, and sustainability metrics.",
        "date": "May 7, 2026",
        "read_time": "3 min",
        "lead": "Building environmentally responsible infrastructure, energy-efficient operations, and sustainability metrics.",
        "tags": ["Sustainability", "Green Cloud", "FinOps", "Efficiency"],
        "body": [
            p("Cloud efficiency and environmental responsibility align more than they conflict. Wasted compute burns money and carbon."),
            h2("Efficiency Levers"),
            p("Right-size instances. Schedule non-production environments. Use autoscaling. Choose regions with renewable energy where latency allows. Optimize code before adding hardware."),
            h2("Measurement"),
            p("Cloud providers publish carbon footprint tools. Tag workloads for accountability. Include sustainability in architecture reviews alongside cost and performance."),
            p("Sustainable cloud is efficient cloud operated with intention."),
        ],
    },
]


def update_blog_index():
    index_path = os.path.join(BLOG, "index.html")
    with open(index_path, encoding="utf-8") as f:
        content = f.read()

    for article in ARTICLES:
        slug = article["slug"]
        href = f'{slug}/'
        # Update placeholder cards matching title
        title = re.escape(article["title"])
        pattern = (
            rf'(<a href="#")([^>]*>\s*'
            rf'<span class="blog-card-tag">[^<]*</span>\s*'
            rf'<h2 class="blog-card-title">{title}</h2>[^<]*'
            rf'<p class="blog-card-excerpt">[^<]*</p>\s*'
            rf'<div class="blog-card-meta">\s*'
            rf'<span class="blog-card-date">📅 )([^<]+)(</span>\s*'
            rf'<span class="blog-card-readtime">)([^<]+)(</span>)'
        )

        def repl(m, href=href, rt=article["read_time"]):
            return f'<a href="{href}"{m.group(2)}{m.group(3)}{m.group(4)}{rt}{m.group(6)}'

        content, count = re.subn(pattern, repl, content, count=1)
        if count == 0:
            print(f"Warning: could not update index for {slug}")

    # Fix linux fundamentals excerpt em dash
    content = content.replace(
        "Every Kubernetes node, every EC2 instance, every containerized workload — underneath it all, Linux is running the show.",
        "Every Kubernetes node, every EC2 instance, every containerized workload. Underneath it all, Linux is running the show.",
    )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    for article in ARTICLES:
        slug = article["slug"]
        out_dir = os.path.join(BLOG, slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        html = html_page(article)
        if "—" in html:
            raise ValueError(f"Em dash found in {slug}")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Created {out_path}")

    update_blog_index()
    print("Updated blog/index.html")


if __name__ == "__main__":
    main()
