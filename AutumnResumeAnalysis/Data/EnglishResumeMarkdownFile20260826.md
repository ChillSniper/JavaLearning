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

icon:douyin ByteDance, Global Payment - Backend Development Intern

:::

::: right

Internship Period: **Apr 2026 - Aug 2026**

:::

Responsibilities: Interned with ByteDance's **Global Payment** team and contributed to the development of the operations center and enforcement center for a **payment risk control platform**. Developed an automated review module for risk escalation tickets, integrated risk mitigation capabilities, and built features for the enforcement platform.

- **Key Contributions**:
- **Automated Review Workflow for Payment CMS Risk Appeals**: Designed and implemented a **configurable rule engine workflow** for three TikTok business lines. Automated reviews accounted for approximately 28% of cases. Over the most recent seven-day production window, the system recorded 115 parent-child ticket reuse events and approximately 36 valid rule matches;
- **Agent-Based Decision Workflow for Risk Appeals**: Contributed to the design and implementation of the Conan intelligent review workflow to support automated appeal reviews after appeal volume doubled across three ROW business lines. After launch, the workflow met production AI review standards with a 92% pass rate;
- **Performance and Reliability Improvements for Enforcement Queries**: Synchronized **two core enforcement tables** to Elasticsearch and adapted both online queries and scheduled jobs to the new data source. Designed an "Elasticsearch-first, database-fallback" strategy for errors or empty results, **maintaining query availability** while reducing migration risk;

    ---

::: left

icon:fa-uniregistry Tuyoo Games, Platform Center - Backend Development Intern

:::

::: right

Internship Period: **Jan 2026 - Mar 2026**

:::

Responsibilities: Interned with Tuyoo Games' **Platform Center** and developed and optimized features for the **Tuyoo Customer Service System**. As the company's shared platform team, the Platform Center supports multiple game project teams and back-office infrastructure by developing reusable services.

- Key Contributions:


- Developed a **payment risk blacklist management module**: Implemented a scheduled blacklist release job with **Redis ZSet** to improve risk control for low-value withdrawal scenarios. Stored release timestamps as scores and combined scheduled scans with a **SetNX** distributed lock to ensure idempotency across multiple service instances;
- Optimized the CRM system's **churned-user re-engagement feature**: Implemented user-level distributed locking with **Redis Pipeline and Lua scripts**. Used **SetNX** for batch lock acquisition and a Lua script for atomic lock release, ensuring idempotent churn-detection jobs under concurrency;
- Integrated and optimized **Apollo Configuration Center**: Used gconf to provide unified access to multiple Apollo Namespaces, implemented OnChange hot updates, cache invalidation, and Worker reloads, and enabled configuration changes to take effect without service restarts, improving configuration maintenance efficiency;

## Project Experience

::: left

### Zhihu Public Opinion Analysis Agent

:::

::: right

Development Period: **Jun 2026 - Present**

:::

- GitHub Link: <https://github.com/ChillSniper/ZhiHu-Analysis-Agent>
- **Project Overview:**

An **analysis workbench** for **public sentiment** analysts. After importing a compliant CSV dataset of Zhihu-style discussions, users can request trend, keyword, and risk analyses in natural language. The system generates reports supported by evidence from original posts and metrics, then routes them for human review.

- **Highlights:**

  - **Designed and implemented a multi-role Workflow Agent execution pipeline**: Decomposed natural-language requests into risk, trend, keyword, and other tasks for parallel execution, followed by evidence validation, report generation, and human review. Isolated the model from the database through seven structured Tools;

  - **Built evidence-based report generation and fact validation**: Implemented report-level fact validation that checks every reported value against Tool outputs. Across 60 offline workflow evaluations, intent, Tool, evidence, and prompt-injection isolation checks all achieved 100%, with P50 latency of 84.36 ms and P95 latency of 129.49 ms;

  - **Designed and implemented a recoverable multi-role Agent DAG execution engine**: Built a recoverable workflow engine that coordinates concurrency through database leases and persists progress with checkpoints, supporting execution resumption after interruptions and SSE trace replay. Reused Tool results through idempotency keys and prevented duplicate report generation.

## Technical Skills

- **Java Fundamentals**: Solid knowledge of collections, reflection, dynamic proxies, and object-oriented design;
- **Golang Fundamentals**: Solid knowledge of slices, goroutines, and channels, with an understanding of the GMP scheduling model and garbage collection;
- **JVM**: Familiar with JVM memory structure and class loading, as well as common garbage collectors and collection algorithms;
- **JUC**: Proficient in core concurrency components, including thread pools, CAS, AQS, and ThreadLocal;
- **MySQL**: Proficient in SQL and query optimization; understands the InnoDB storage engine, including index structures, transaction isolation, locking, and MVCC;
- **Redis**: Familiar with RDB/AOF persistence and memory eviction policies, as well as solutions for cache penetration, cache breakdown, and cache avalanche;
- **Frameworks**: Proficient in Spring Boot and Gin + GORM, with a solid understanding of AOP internals and approaches to resolving circular dependencies;
- **Middleware**: Familiar with Kafka, including its messaging model and consumer acknowledgment mechanisms;
- **AI Applications**: Familiar with large language model API integration and prompt design; capable of developing business features with AI tool calling and Agent workflows;