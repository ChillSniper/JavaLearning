## Xuecheng Lu

::: left

icon:phone Phone: 18795702368

icon:weixin WeChat: XueCheng_Lu0517

:::

::: right

[icon:email Email: 3242473480@qq.com](mailto:3242473480@qq.com)

[icon:github https://github.com/ChillSniper](https://github.com/ChillSniper)

:::

## Education

::: left

**Jilin University** B.S. in Computer Science and Technology

:::

::: right

**Sep 2023 - Jun 2027**

:::

**Honors & Awards:**

- National First Prize, China University Computer Game Competition
- First-Class University Scholarship, 2023-2024
- Second-Class University Scholarship, 2024-2025

## Internship Experience

::: left

### ByteDance, Global Payment - Backend Software Engineer Intern

:::

::: right

Internship Period: **Apr 2026 - Present**

:::

- **Overview:** Interned with ByteDance's **Global Payment** team and contributed to the development of the Operations Center, Penalty Center, and Appeal Center within the payment risk control platform. Responsible for developing an automated review module for risk escalation tickets, integrating risk mitigation capabilities, and building appeal data feedback pipelines.
- **Key Contributions:**
  - **Payment CMS Automated Review Pipeline for Risk-Related Customer Complaints:** Designed and implemented a **configuration-driven rule engine pipeline** based on TCC and govaluate for three TikTok business lines. Integrated Appeal Center snapshots, Rep/Arena lists, SKY actions, and ByteHi ticket-closing capabilities. Supported parent-child ticket result reuse, automated responses, allowlisting, ticket closure, and automated actions such as Withdraw Link and Forget PIN. Automated reviews accounted for approximately 28% of all reviews; over the latest seven-day period, the system recorded 115 parent-child result reuses and approximately 36 effective rule matches.
  - **Agent-Based Intelligent Decision Pipeline for Risk-Related Appeals:** To address doubled appeal volumes and a low automated review rate across three business lines in the ROW region, contributed to the design of an intelligent review pipeline consisting of a **document information extraction Agent, authenticity verification Agent, consistency checking Agent, and deterministic TCC rules**. Designed and implemented improvements to the Conan pipeline to aggregate ticket, KYC, PI, email, and address information into Agent review results. After launch, approval decisions made by the Agent achieved 92% accuracy, meeting the production standard for AI-based decision-making.
  - **Performance and Reliability Improvements for the Penalty Query Pipeline:** To resolve frequent timeouts caused by complex and range queries as penalty data continued to grow, synchronized **two core penalty tables** to Elasticsearch and adapted both online queries and scheduled jobs to the new data source. Designed a compatibility strategy that queried Elasticsearch first and fell back to the database on errors or empty results, preserving query availability while reducing migration risk and resolving timeout issues for selected operational queries.
  - **Penalty Platform Capabilities and Compliance Engineering:** Contributed to the separation of payment and financial entities in the Indonesian market and to PCI-sensitive card information remediation. Implemented dynamic downstream routing and `instrument_id -> PipoCardId` mapping to **meet cross-market compliance requirements**. Integrated multidimensional atomic enforcement capabilities for UK Visa virtual cards and TTPay, including card freezing/unfreezing and restrictions on incoming/outgoing account transactions. Added **real-time feature APIs** exposing penalty status, latest penalty/removal timestamps, and operator information to support upstream risk strategy decisions.
  - **Automated Enforcement and Appeal Pipeline Development:** Built an **automated Fraud Chargeback response workflow** that consumes FCB messages, retrieves recurring payment agreement IDs from events, and **reuses existing penalty capabilities** to automatically cancel subscriptions, reducing manual processing and potential financial losses caused by delayed actions. Launched online CVV redaction for bank cards in the **live-streaming risk appeal pipeline**, allowing eligible users to continue their appeals through personnel authorization checks and sensitive data masking. Encapsulated appeal activities as **asynchronous risk events** and published them to MQ, providing appeal behavior data to the risk strategy team.

::: left

### Tuyoo Games, Platform Center - Backend Software Engineer Intern

:::

::: right

Internship Period: **Jan 2026 - Mar 2026**

:::

- **Overview:** Interned with the company's **Platform Center**, where I developed and optimized features for the **Tuyoo customer service system**. As a shared platform team, the Platform Center supports multiple game project teams and backend infrastructure by developing reusable service systems.
- **Key Contributions:**
  - **Developed a Payment Risk Blacklist Management Module:** Improved risk control for small-amount withdrawal scenarios by implementing a scheduled blacklist expiration task with **Redis ZSet**. Stored expiration timestamps as scores and used **ZRANGEBYSCORE** for scheduled scanning together with a **SetNX-based distributed lock** for highly available task scheduling, ensuring idempotency in a multi-instance environment.
  - **Integrated and Optimized Apollo Configuration Center:** Encapsulated multi-namespace configuration binding through the **gconf** component and implemented a **configuration hot-reload listener**. When Apollo configurations changed, the system dynamically updated in-memory configuration objects through **OnChange** callbacks without requiring service restarts, significantly improving configuration flexibility and operational efficiency.
  - **Optimized the CRM Churn Recall Feature:** Implemented user-level distributed locking with **Redis Pipeline and Lua scripts**, using **SetNX** for batch lock acquisition and Lua scripts for atomic lock release to ensure idempotency in concurrent churn-detection tasks. Upgraded the original do-not-disturb feature into a reusable **tag system**. Queried users with hidden tags through the DAO-layer **GetHiddenTagUIDs** method and dynamically filtered churn lists using the **WithExcludeUIDs** option.

## Project Experience

::: left

### Zhihu Public Opinion Analysis Agent

:::

::: right

Development Period: **Jun 2026 - Present**

:::

- GitHub Link: <https://github.com/ChillSniper/ZhiHu-Analysis-Agent>
- **Project Overview:**

A **public opinion analysis workbench** built with FastAPI, Vue 3, and an OpenAI-compatible provider. The system supports importing lawfully obtained CSV datasets containing Zhihu-style public discussions. Users can initiate **analysis tasks** through natural-language instructions, after which a Planner generates a structured DAG and invokes **controlled analysis tools**. Evidence Verifier and Claim Verifier components validate facts and supporting evidence before the report enters human review and is finalized as a replayable report.

- **Key Contributions:**
  - **Designed and Implemented a Multi-Role Workflow Agent Pipeline:** Built a bounded workflow consisting of Planner -> Parallel Workers -> Evidence Verifier -> Report Synthesizer -> Claim Verifier -> Human Review. Agents can access business data only through seven registered tools, each with strict ArgsModel/ResultModel definitions and input/output JSON Schemas. This isolates the model from direct ORM/SQL access and reduces the risks of prompt injection and unsupported generation.
  - **Built Evidence-Driven Report Generation and Fact Verification:** Required each factual Claim to include fields such as value, unit, and operator. The Verifier traces each Claim back to the corresponding path in the actual Tool Result and validates its values. Across an offline evaluation of 60 tasks, intent recognition, tool selection, evidence citation, and prompt-injection isolation all achieved 100%. Offline execution latency reached P50 of 84.36 ms and P95 of 129.49 ms, with an average of 6.45 steps per task.
  - **Designed and Implemented a Recoverable Multi-Role Agent DAG Execution Engine:** Used versioned Pydantic WorkflowState models and checkpoint persistence to track node progress. Implemented concurrent task claiming and timeout recovery through SQLAlchemy conditional UPDATE operations, Run/Task lease tokens, and heartbeat mechanisms. Supported execution trace resumption through a monotonic event stream and SSE Last-Event-ID, while preventing duplicate business results through ToolCall idempotency keys and a unique constraint on agent_run_id.

## Technical Skills

- **Java:** Proficient in collections, reflection, dynamic proxies, and object-oriented design;
- **Golang:** Proficient in slices, goroutines, and channels; familiar with the GMP scheduling model and garbage collection;
- **JVM:** Familiar with JVM memory structure, class loading, common garbage collectors, and garbage collection algorithms;
- **Java Concurrency:** Familiar with thread pools, CAS, AQS, ThreadLocal, and other core JUC components;
- **MySQL:** Proficient in SQL development and optimization; familiar with the InnoDB storage engine, including index structures, transaction isolation, locking mechanisms, and MVCC;
- **Redis:** Familiar with RDB/AOF persistence and memory eviction policies, as well as solutions for cache penetration, cache breakdown, and cache avalanche;
- **Frameworks:** Proficient in Spring Boot and Gin + GORM; familiar with the underlying principles of AOP and solutions to circular dependencies;
- **Middleware:** Familiar with Kafka, including its messaging model and consumer acknowledgment mechanisms.