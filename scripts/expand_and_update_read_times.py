#!/usr/bin/env python3
"""Expand short blog posts and recalculate accurate read times."""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
WPM = 200
MARKER = '<div class="blog-tags">'

# Additional sections inserted before tags. Target: 3-4 min standard, 5-6 min architecture.
EXPANSIONS = {
    "agentic-ai-in-india": """
        <h2>Why India Is Uniquely Positioned</h2>
        <p>India combines scale, digital public infrastructure, and a young engineering workforce in a way few countries can match. Aadhaar, UPI, and the India Stack proved that population-scale systems can be built with openness and interoperability. Agentic AI can sit on top of this foundation, not replace it. The opportunity is not to copy Western AI playbooks, but to design agents that understand regional languages, intermittent connectivity, and last-mile delivery constraints.</p>
        <p>In my work leading cloud and AI platform initiatives, the teams that succeed treat agents as socio-technical systems. They invest in human-in-the-loop design, local language evaluation datasets, and governance frameworks before they chase model benchmarks.</p>
        <h2>Design Principles for Responsible Deployment</h2>
        <p>Start with narrow, high-impact domains where errors are detectable and escalation paths exist. Healthcare triage agents should route to ANMs, not diagnose independently. Education agents should augment teachers, not replace classroom relationships. Governance agents should support officials with evidence, not make autonomous enforcement decisions.</p>
        <p>Build feedback loops from day one. Capture when agents fail, when users override recommendations, and when outcomes diverge from intent. Use this data to retrain, constrain, or retire capabilities. Transparency builds trust faster than accuracy alone.</p>
        <h2>What Success Looks Like in Five Years</h2>
        <p>Success is not universal chatbots. It is measurable improvement in PHC throughput, student learning outcomes in rural classrooms, faster emergency response at public events, and higher farm incomes through timely, contextual advice. Agentic AI in India should be judged by lives improved, not demos shipped.</p>
""",
    "api-governance-at-scale": """
        <h2>Versioning and Deprecation</h2>
        <p>Publish a versioning policy and stick to it. Breaking changes require a new major version, a migration guide, and a sunset date for the old version. Clients need at least one release cycle to adapt. Internal services are not exempt: undocumented breaking changes destroy trust as quickly as public API changes do.</p>
        <h2>Operational Governance</h2>
        <p>Rate limits protect your platform and signal fair usage. Authentication should be consistent across services: OAuth2, API keys, or mutual TLS, but not a mix without clear rules. Log every API call with correlation IDs so support and engineering can trace issues across service boundaries.</p>
        <h2>Measuring API Health</h2>
        <p>Track adoption, error rates, latency percentiles, and time-to-first-successful-call for new consumers. APIs with declining usage may be candidates for retirement. APIs with high error rates need better documentation or design fixes, not more consumers.</p>
""",
    "building-internal-developer-platforms": """
        <h2>Golden Paths That Teams Actually Use</h2>
        <p>A golden path should take a developer from empty repo to running in staging in under an hour. That means templates include CI/CD, observability, security scanning, and documentation stubs. If teams fork the template and delete half of it, your platform is too heavy. If they bypass it entirely, your platform is too rigid. Interview users monthly.</p>
        <h2>Platform Team Operating Model</h2>
        <p>Platform teams are product teams. They need a roadmap, SLAs, and support channels. Treat internal developers as customers. Publish uptime for the platform itself. When the IDP is down, every product team stops shipping.</p>
""",
    "cloud-cost-optimization": """
        <h2>Visibility Before Cuts</h2>
        <p>You cannot optimize what you cannot attribute. Enforce tagging standards before launching cost initiatives. Map spend to teams, environments, and products. Chargeback or showback creates accountability. Finance and engineering should review the same dashboard monthly.</p>
        <h2>Architectural Cost Decisions</h2>
        <p>Multi-AZ redundancy costs more than single-AZ. Cross-region replication doubles storage and transfer. Kubernetes clusters have baseline cost even at zero replicas. Document these tradeoffs when teams request HA. Sometimes the business accepts risk to save budget. That is a valid decision when it is explicit.</p>
""",
    "cloud-networking-vpcs": """
        <h2>Subnet Design Patterns</h2>
        <p>Use /24 subnets per availability zone for application tiers unless you have a documented reason to go smaller or larger. Reserve IP space for load balancers, NAT gateways, and future growth. Plan pod CIDR ranges separately when using Kubernetes with VPC-native networking to avoid overlap with node subnets.</p>
        <h2>Hybrid Connectivity</h2>
        <p>Site-to-site VPN is fast to set up but limited in throughput. Dedicated interconnect suits steady, high-volume traffic between on-premises data centers and cloud. Always design failover: a single VPN tunnel is a single point of failure.</p>
""",
    "compliance-as-code": """
        <h2>Policy Libraries</h2>
        <p>Start with a small set of high-impact policies: encryption at rest enabled, public access blocked, mandatory tags present, and approved instance types only. Expand gradually. Policies that block every deployment get disabled. Policies that catch real issues get maintained.</p>
        <h2>Audit Readiness</h2>
        <p>Store policy evaluation results with timestamps and resource identifiers. Auditors want evidence of continuous compliance, not screenshots from the day before the audit. Git history for infrastructure changes provides the who, what, and when for every environment change.</p>
""",
    "contributing-open-source": """
        <h2>Your First Pull Request</h2>
        <p>Read CONTRIBUTING.md. Search closed issues before opening new ones. Reproduce bugs with minimal examples. Follow the project's code style without debate. Keep PRs focused: one logical change per pull request. Respond to review feedback promptly and professionally.</p>
        <h2>Building Reputation</h2>
        <p>Consistent small contributions matter more than one large dump. Help triage issues. Improve documentation. Fix flaky tests. Maintainers remember reliable contributors when they need help on harder problems.</p>
""",
    "data-pipelines-etl": """
        <h2>Choosing Batch vs. Stream</h2>
        <p>Batch suits daily reports, billing cycles, and historical analysis. Stream suits fraud detection, live dashboards, and event-driven automation. Many systems use both: stream for real-time signals, batch for reconciliation and correction.</p>
        <h2>Data Quality Gates</h2>
        <p>Validate schema, row counts, and null rates at pipeline boundaries. Fail fast when upstream data is corrupt rather than propagating bad data to dashboards executives trust.</p>
""",
    "devops-culture-beyond-tools": """
        <h2>Shared On-Call as a Cultural Signal</h2>
        <p>When developers share on-call rotation with operators, priorities align quickly. Latency regressions get fixed. Logging improves. Runbooks get written because the people who write code answer pages at night.</p>
        <h2>Leadership Behaviors That Matter</h2>
        <p>Managers who celebrate learning from incidents over hiding them build resilient teams. Reward improvements to systems, not heroics during outages caused by preventable failures.</p>
""",
    "edge-computing-sovereign-infrastructure": """
        <h2>Data Residency Requirements</h2>
        <p>Sovereign infrastructure is not just about where data is stored. It is about who can access it, under what legal jurisdiction, and whether foreign cloud operators have technical access. Edge nodes in-country with local key management address all three concerns.</p>
        <h2>Operating at the Edge</h2>
        <p>Edge sites lack on-site experts. Design for remote operations: out-of-band management, local log buffering, and automated recovery playbooks. Test disconnected scenarios before production deployment.</p>
""",
    "gitops-declarative-infrastructure": """
        <h2>Repository Structure</h2>
        <p>Separate repos for infrastructure, application manifests, and policy. Use environment branches or overlay directories with Kustomize. Avoid one giant repo that requires every team to have write access to production configuration.</p>
        <h2>Handling Secrets in GitOps</h2>
        <p>Never commit plaintext secrets. Use sealed secrets, external secrets operators, or cloud-native secret stores referenced from manifests. Rotate credentials on a schedule and automate the rotation through the same GitOps pipeline.</p>
        <h2>Rollback Strategy</h2>
        <p>Git revert is your rollback. Tag releases that reach production. Practice rollbacks in staging so on-call engineers know the steps before an incident forces them to learn.</p>
""",
    "green-cloud-sustainable-computing": """
        <h2>Scheduling and Environment Lifecycle</h2>
        <p>Non-production environments running 24/7 waste energy and money. Schedule shutdowns nights and weekends. Use smaller instance types in dev. Delete unused volumes and snapshots quarterly.</p>
        <h2>Carbon-Aware Decisions</h2>
        <p>Some cloud regions run on higher renewable energy mixes. Where latency allows, place batch workloads in greener regions. Report carbon metrics alongside cost in quarterly reviews.</p>
""",
    "growing-cloud-career": """
        <h2>Building Depth and Breadth</h2>
        <p>Pick one cloud deeply, then expand horizontally. AWS, Azure, or GCP fundamentals transfer once you understand IAM, networking, compute, and storage patterns. Certifications validate baseline knowledge but projects prove capability.</p>
        <h2>Portfolio Over Promises</h2>
        <p>Document migrations you led, cost savings you delivered, and incidents you resolved. Write about what you learned. A public blog or conference talk differentiates you in a crowded market.</p>
""",
    "iac-best-practices": """
        <h2>Module Design</h2>
        <p>Modules should do one thing well. Expose clear variables with validation rules and sensible defaults. Document required IAM permissions. Version modules with semantic versioning so consumers can upgrade safely.</p>
        <h2>State Management</h2>
        <p>Use remote state with locking. Never commit state files to Git. Split state by blast radius: networking, shared services, and application infrastructure in separate backends so a bad apply does not take down everything.</p>
""",
    "kubernetes-networking-cni": """
        <h2>Choosing a CNI Plugin</h2>
        <p>Evaluate based on performance requirements, network policy needs, observability features, and operational familiarity. Calico suits policy-heavy environments. Cilium adds eBPF-based visibility. Flannel is simpler but less feature-rich. Test with your actual traffic patterns before standardizing.</p>
        <h2>Service Mesh Decision</h2>
        <p>Do not adopt a service mesh because it is trendy. Adopt when you need mutual TLS everywhere, advanced traffic shaping, or consistent observability across polyglot services. Meshes add operational complexity that must be justified.</p>
""",
    "leading-technical-teams": """
        <h2>One-on-Ones That Matter</h2>
        <p>Ask about blockers, growth goals, and team health. Do not use one-on-ones for status updates that belong in standups. Protect this time. Engineers who feel heard stay longer and perform better.</p>
        <h2>Technical Decision Records</h2>
        <p>Document significant architecture decisions with context, options considered, and tradeoffs accepted. Future teams will thank you when they ask why something was built a certain way and you are not available to answer.</p>
""",
    "microservices-on-aws-eks": """
        <h2>Implementation Checklist</h2>
        <p>Provision EKS with private API endpoints where possible. Enable IRSA for pod-level AWS permissions. Deploy the AWS Load Balancer Controller before exposing services. Configure cluster autoscaling and horizontal pod autoscaling per service. Set resource requests and limits on every deployment.</p>
        <h2>Production Hardening</h2>
        <p>Enable control plane logging. Restrict security groups to minimum required ports. Use separate AWS accounts per environment. Scan images in ECR on push. Run pod security standards or OPA policies to block privileged containers.</p>
        <h2>When to Choose EKS</h2>
        <p>EKS fits teams already invested in AWS who need Kubernetes without managing the control plane. If your workloads are simple and stateless, ECS or Lambda may be simpler. Choose EKS when service count, team autonomy, or portability requirements justify Kubernetes operational overhead.</p>
""",
    "microservices-on-azure-aks": """
        <h2>Implementation Checklist</h2>
        <p>Create AKS with Azure CNI and plan IP address space carefully. Integrate with Azure Active Directory for cluster admin access. Deploy ingress controller and cert-manager for TLS. Configure Azure Monitor container insights from day one. Use Azure Key Vault provider for secrets.</p>
        <h2>Production Hardening</h2>
        <p>Enable Azure Policy for Kubernetes. Use private clusters for production where network requirements allow. Separate node pools for system and user workloads. Apply pod disruption budgets for critical services.</p>
        <h2>When to Choose AKS</h2>
        <p>AKS is the natural choice for enterprises standardized on Azure with Microsoft identity, hybrid connectivity through ExpressRoute, and existing Azure DevOps pipelines. Evaluate AKS when Kubernetes portability matters but Azure managed services handle persistence.</p>
""",
    "microservices-on-gcp-gke": """
        <h2>Implementation Checklist</h2>
        <p>Enable Workload Identity before deploying applications. Use regional clusters for HA. Configure Network Policies with Calico or Cilium. Set up Cloud Build triggers linked to your repository. Enable GKE cost allocation labels for FinOps visibility.</p>
        <h2>Production Hardening</h2>
        <p>Enable Binary Authorization to enforce signed images. Use private GKE clusters with authorized networks. Configure maintenance windows and release channels appropriate to your risk tolerance. Back up etcd state and test cluster recovery.</p>
        <h2>When to Choose GKE</h2>
        <p>GKE suits teams leveraging BigQuery, Pub/Sub, and other GCP data services alongside containerized applications. Google operates Kubernetes upstream, so GKE often receives features first. Choose GKE when data analytics and ML pipelines share infrastructure with microservices.</p>
""",
    "microservices-on-oci-oke": """
        <h2>Implementation Checklist</h2>
        <p>Deploy OKE on flexible shapes for cost efficiency. Configure OCI IAM policies for cluster and node pool management. Set up OCIR in the same region as the cluster. Use OCI Load Balancer for ingress with proper backend set health checks.</p>
        <h2>Production Hardening</h2>
        <p>Store secrets in OCI Vault and reference them from Kubernetes secrets via CSI drivers. Enable OCI Cloud Guard for security posture management. Use compartment isolation per environment. Monitor with OCI APM and Logging.</p>
        <h2>When to Choose OKE</h2>
        <p>OKE fits organizations with Oracle database estates, data residency requirements in specific regions, or commercial commitments to OCI. Kubernetes skills transfer directly. Managed services handle the control plane while OCI native services handle persistence and identity.</p>
""",
    "mlops-operationalizing-models": """
        <h2>Model Registry and Versioning</h2>
        <p>Every trained model gets a version, training dataset reference, evaluation metrics, and approval status. Production deployments pin to specific versions. Rollback means deploying the previous registered version, not retraining under pressure.</p>
        <h2>Serving and Monitoring</h2>
        <p>Monitor prediction latency, throughput, and error rates like any other service. Track input data distributions for drift. Alert when accuracy on holdout samples degrades. Schedule retraining or trigger it automatically when drift exceeds thresholds.</p>
""",
    "monolith-to-microservices": """
        <h2>Identifying Service Boundaries</h2>
        <p>Look for natural seams: different release cadences, different scaling needs, or different team ownership. Domain-driven design bounded contexts help. Do not split along technical layers only (API service, database service) unless you enjoy distributed monolith pain.</p>
        <h2>Data Ownership Rules</h2>
        <p>Each service owns its data store. Other services access data through APIs, not shared databases. Shared databases between services recreate monolith coupling with network latency added.</p>
""",
    "multi-cloud-strategies": """
        <h2>Connectivity and Identity Federation</h2>
        <p>Multi-cloud networking requires planned connectivity: cloud exchange providers, VPN meshes, or dedicated interconnects per provider. Identity federation across clouds prevents duplicate user directories and inconsistent access policies. SAML or OIDC with a central IdP is the common pattern.</p>
        <h2>Avoiding the Lowest Common Denominator</h2>
        <p>Abstracting everything to work identically on four clouds often means using none of them well. Allow provider-specific optimizations where they deliver clear value. Standardize interfaces and governance, not every implementation detail.</p>
        <h2>Migration Waves</h2>
        <p>Migrate in waves with clear success criteria per wave. Wave one might be stateless web tiers. Wave two adds databases with tested backup and restore. Never migrate everything at once. Always maintain rollback capability to the previous environment until the new one proves stable in production.</p>
""",
    "observability-vs-monitoring": """
        <h2>Instrumenting Effectively</h2>
        <p>Add correlation IDs at the edge and propagate through every service call. Structure logs as JSON for parsing. Use consistent metric naming conventions. Sample traces in high-throughput paths but never sample error traces.</p>
        <h2>Alert Design</h2>
        <p>Every alert should be actionable by the on-call engineer receiving it. If the response is always "wait and see," it should be a dashboard, not a page. Review alerts quarterly and delete noisy ones ruthlessly.</p>
""",
    "on-call-excellence": """
        <h2>Runbook Quality</h2>
        <p>A good runbook answers: What does this alert mean? How do I confirm it is real? What are the first three diagnostic steps? When do I escalate? Link runbooks directly from alert notifications.</p>
        <h2>Post-Incident Learning</h2>
        <p>Blameless postmortems focus on system improvements, not individual fault. Action items get owners and deadlines. Track completion. Repeated incidents without completed action items signal organizational failure, not technical failure.</p>
""",
    "performance-optimization": """
        <h2>Profiling Workflow</h2>
        <p>Reproduce the slow path reliably. Profile before optimizing. Fix the largest bottleneck first. Measure again. Repeat. Optimizing code that is not on the critical path wastes time.</p>
        <h2>Infrastructure Scaling</h2>
        <p>Horizontal scaling solves capacity problems. Vertical scaling solves inefficient single-node performance. Autoscaling policies need tuning: scale-up fast, scale-down slow to avoid flapping.</p>
""",
    "rto-rpo-business-continuity": """
        <h2>DR Testing Cadence</h2>
        <p>Run tabletop exercises quarterly. Execute full failover tests annually. Document actual RTO and RPO achieved versus targets. Update architecture when gaps exceed business tolerance.</p>
        <h2>Backup Validation</h2>
        <p>Backups that have never been restored are assumptions. Automate restore tests to an isolated environment monthly. Verify data integrity and application startup, not just backup job success.</p>
""",
    "scalable-ml-pipelines": """
        <h2>Feature Stores and Reproducibility</h2>
        <p>Version training features alongside model artifacts. The same feature computation logic should power training and inference. Drift between training and serving features silently degrades model quality in production.</p>
        <h2>Scaling Training and Inference Separately</h2>
        <p>Training is batch-heavy and GPU-intensive. Inference is latency-sensitive and often CPU-sufficient. Design separate infrastructure for each phase. Autoscale inference on request rate, not on training schedule.</p>
""",
    "serverless-when-to-use": """
        <h2>Cost Modeling</h2>
        <p>Serverless is cheap at low volume and expensive at sustained high volume. Model your expected invocation count, duration, and memory before choosing serverless over containers. The crossover point often surprises teams.</p>
        <h2>Cold Start Mitigation</h2>
        <p>Provisioned concurrency, smaller runtimes, and keeping dependencies minimal reduce cold starts. For latency-sensitive APIs, measure P99 cold start impact before committing to serverless.</p>
""",
    "sql-vs-nosql": """
        <h2>Migration Considerations</h2>
        <p>Moving from SQL to NoSQL to gain scale often fails when the application relies on joins and transactions. Denormalize deliberately and accept consistency tradeoffs before migrating. Sometimes read replicas and partitioning solve SQL scale problems without changing database category.</p>
        <h2>Operational Overhead</h2>
        <p>Managed relational databases reduce operational burden significantly. Self-managed NoSQL clusters require expertise in sharding, replication, and backup. Factor operations cost into the decision, not just license or storage cost.</p>
""",
    "technology-trends-2026": """
        <h2>AI Platform Engineering</h2>
        <p>Enterprises are moving from AI experiments to AI platforms with governance, cost controls, and evaluation frameworks. The platform team owns model access, prompt versioning, and guardrails. Product teams consume AI capabilities through APIs, not by calling models directly.</p>
        <h2>Cost and Sustainability Pressure</h2>
        <p>After years of growth-first cloud spending, FinOps and carbon awareness are board-level topics. Architects who optimize for cost and energy efficiency alongside performance will be in demand.</p>
""",
    "testing-infrastructure": """
        <h2>CI Pipeline Integration</h2>
        <p>Run terraform validate and plan on every pull request. Apply only from protected branches. Use separate cloud accounts for CI testing to prevent accidents. Tear down ephemeral environments automatically after tests complete.</p>
        <h2>Chaos Experiments</h2>
        <p>Start with controlled experiments: terminate a single node, inject latency, fill disk. Document system behavior. Expand scope as confidence grows. Never run chaos in production without stakeholder approval and rollback plans.</p>
""",
    "zero-trust-architecture": """
        <h2>Identity-Centric Access</h2>
        <p>Replace long-lived credentials with short-lived tokens. Use conditional access policies based on device posture, location, and risk signals. Review access permissions quarterly and remove stale grants.</p>
        <h2>Network Segmentation</h2>
        <p>Default deny between services. Allow only required ports and protocols. Use service mesh or network policies to enforce segmentation that security groups alone cannot provide inside Kubernetes.</p>
""",
}

EXPANSIONS_ROUND2 = {
    "microservices-on-aws-eks": """
        <h2>Networking Deep Dive</h2>
        <p>The AWS VPC CNI assigns real VPC IP addresses to pods, which simplifies integration with existing security groups and network appliances but requires careful IP planning. Ensure your VPC CIDR and subnet sizes accommodate peak pod count. Use custom networking or prefix delegation for large clusters. Security groups attach directly to pod ENIs in some configurations, giving fine-grained control at the cost of complexity.</p>
        <p>For service-to-service communication inside the cluster, prefer ClusterIP services with network policies restricting east-west traffic. Expose only the ingress controller and API gateway through the ALB. Internal microservices should never have public endpoints.</p>
        <h2>Observability Stack</h2>
        <p>Deploy CloudWatch Container Insights or Prometheus with AMP (Amazon Managed Prometheus) for metrics. Ship logs to CloudWatch Logs with structured JSON. Enable X-Ray tracing on ingress and critical services. Correlate traces with logs using shared trace IDs. Dashboards should show golden signals per service: latency, traffic, errors, and saturation.</p>
""",
    "microservices-on-azure-aks": """
        <h2>Networking Deep Dive</h2>
        <p>Azure CNI assigns VNet IPs to pods, similar to AWS. Plan subnet sizes for nodes and pods together. Azure Network Policy or Cilium enforces east-west rules. Private Link connects to PaaS services without public internet exposure. ExpressRoute or VPN connects on-premises networks for hybrid workloads.</p>
        <h2>Observability Stack</h2>
        <p>Container Insights collects metrics and logs automatically. Application Insights provides APM with distributed tracing when SDKs are instrumented. Create workbooks that correlate ingress latency with backend service health. Alert on pod restart loops and OOMKilled events before users report outages.</p>
""",
    "microservices-on-gcp-gke": """
        <h2>Networking Deep Dive</h2>
        <p>GKE VPC-native clusters allocate pod IPs from your subnet ranges. Alias IP ranges maximize IP efficiency. Firewall rules and Network Policies layer defense. Private Service Connect reaches Google APIs without public routing. Cloud NAT provides outbound internet for private nodes.</p>
        <h2>Observability Stack</h2>
        <p>Cloud Monitoring dashboards track pod CPU, memory, and restart counts. Cloud Logging aggregates container stdout with queryable labels. Cloud Trace links spans across microservices. Error Reporting groups similar stack traces for faster triage.</p>
""",
    "microservices-on-oci-oke": """
        <h2>Networking Deep Dive</h2>
        <p>OKE VCN-native pod networking integrates pods into your virtual cloud network. Security lists and NSGs control traffic at the VCN level. Service Gateway provides private access to OCI services. FastConnect links on-premises data centers with predictable latency.</p>
        <h2>Observability Stack</h2>
        <p>OCI Monitoring tracks cluster and node health metrics. Logging ingests application logs with search and retention policies. APM traces requests across services and highlights slow database calls. Set alarms on API error rates and certificate expiry.</p>
""",
    "multi-cloud-strategies": """
        <h2>Common Pitfalls</h2>
        <p>Teams often adopt multi-cloud for executive preference rather than technical need. This creates operational burden without corresponding benefit. Another pitfall is duplicating entire platforms on each cloud instead of placing workloads where each provider excels. A third is inconsistent security baselines that create the weakest-link problem across providers.</p>
        <h2>Getting Started</h2>
        <p>Inventory existing workloads and classify by cloud fit, compliance requirements, and migration complexity. Establish a cloud center of excellence with representatives from security, networking, finance, and engineering. Pilot one workload migration per target cloud before committing to broad strategy.</p>
""",
    "gitops-declarative-infrastructure": """
        <h2>Common Pitfalls</h2>
        <p>Auto-syncing to production without approval gates causes incidents. Storing secrets in Git, even encrypted poorly, creates risk. Monolithic repos where every team shares write access lead to accidental cross-team changes. Drift detection without remediation process just generates noise.</p>
        <h2>Getting Started</h2>
        <p>Pick one non-critical application and one environment. Set up Argo CD or Flux with a simple repo structure. Practice a full promotion cycle from dev to staging. Document the workflow and train one product team before expanding platform-wide.</p>
""",
    "kubernetes-networking-cni": """
        <h2>Common Pitfalls</h2>
        <p>Choosing a CNI without testing at production traffic volumes leads to performance surprises. Ignoring IP address exhaustion in large clusters causes scheduling failures. Deploying a service mesh before mastering basic ingress and network policies adds complexity without benefit.</p>
        <h2>Getting Started</h2>
        <p>Deploy a test cluster with your candidate CNI. Run network policy tests between namespaces. Measure pod-to-pod latency under load. Document the debugging workflow for DNS failures and connection timeouts before going to production.</p>
""",
    "agentic-ai-in-india": """
        <h2>Building Local Capacity</h2>
        <p>India needs more engineers who understand both AI systems and domain contexts: agriculture, healthcare, education, and governance. Universities and industry should collaborate on curricula that combine machine learning with field deployment experience. Open-source Indian language datasets and evaluation benchmarks will accelerate responsible innovation.</p>
""",
}

# Generic round-2 blocks for remaining short articles
GENERIC_PITFALLS = """
        <h2>Common Pitfalls</h2>
        <p>Adopting tools before defining outcomes leads to expensive experiments without business value. Copying another organization's architecture without understanding your constraints creates fragile systems. Skipping documentation means every new team member relearns lessons the hard way.</p>
        <h2>Getting Started</h2>
        <p>Define success metrics before implementation. Start with the smallest scope that proves value. Review results with stakeholders weekly during the first month. Iterate based on evidence, not assumptions.</p>
"""


def expand_articles():
    all_expansions = {**EXPANSIONS, **EXPANSIONS_ROUND2}
    for slug, html_block in all_expansions.items():
        path = os.path.join(BLOG, slug, "index.html")
        if not os.path.isfile(path):
            print(f"skip missing: {slug}")
            continue
        with open(path, encoding="utf-8") as f:
            content = f.read()
        if MARKER not in content:
            continue
        # Insert only if this block's first h2 is not already present
        first_h2 = re.search(r"<h2>([^<]+)</h2>", html_block)
        if first_h2 and first_h2.group(1) in content:
            continue
        content = content.replace(MARKER, html_block + "\n\n        " + MARKER, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"expanded: {slug}")

    # Apply generic expansion to articles still under 500 words without Common Pitfalls
    for name in os.listdir(BLOG):
        path = os.path.join(BLOG, name, "index.html")
        if not os.path.isfile(path) or name == "linux-fundamentals":
            continue
        with open(path, encoding="utf-8") as f:
            content = f.read()
        words = len(extract_text(content).split())
        if words >= 500 or "Common Pitfalls" in content:
            continue
        if MARKER not in content:
            continue
        content = content.replace(MARKER, GENERIC_PITFALLS + "\n\n        " + MARKER, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"generic expand: {name}")


def extract_text(html):
    match = re.search(r'<article class="blog-content">(.*?)</article>', html, re.DOTALL)
    if not match:
        return ""
    text = re.sub(r"<[^>]+>", " ", match.group(1))
    return re.sub(r"\s+", " ", text).strip()


def read_time_label(word_count):
    minutes = max(1, round(word_count / WPM))
    return f"{minutes} min"


def update_read_times():
    manifest = []
    for name in sorted(os.listdir(BLOG)):
        path = os.path.join(BLOG, name, "index.html")
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        words = len(extract_text(html).split())
        label = read_time_label(words)
        html = re.sub(
            r'(<div class="blog-meta-item">⏱️ )[^<]+(</div>)',
            rf"\g<1>{label} read\2",
            html,
            count=1,
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        manifest.append((name, words, label))

    index_path = os.path.join(BLOG, "index.html")
    with open(index_path, encoding="utf-8") as f:
        index = f.read()
    for slug, _, label in manifest:
        pattern = rf'(<a href="{re.escape(slug)}/"[^>]*>.*?<span class="blog-card-readtime">)[^<]+(</span>)'
        index = re.sub(pattern, rf"\g<1>{label}\2", index, count=1, flags=re.DOTALL)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index)

    print("\nRead times after expansion:")
    for name, words, label in sorted(manifest, key=lambda x: -x[1]):
        print(f"  {label:>6}  {words:4d} words  {name}")


if __name__ == "__main__":
    expand_articles()
    update_read_times()
