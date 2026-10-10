# NYC CityJobs Matcher — Prompt-Based Skill

[中文](#中文) · [English](#english)

## 中文

**定位：** 面向 ChatGPT Scheduled Tasks、Meta Muse 及其他网页端 Agent 的纯提示词 `SKILL.md`，不运行 Python、数据库或自建爬虫服务。宿主 Agent 负责搜索官方职位、读取 JD、按规则判断、跨次状态（如支持）、任务调度和通知。

### 主要功能
1. 用户明确选择搜索范围时，严格按范围检索，不限定 IT 或特定职业。
2. 用户不知道适合哪些岗位时，先收集不含雇主、人名及隐私信息的工作经历，再推断职业方向。
3. 每条职位实际阅读 JD：分别检查必须资格、Civil Service 任用条件、日常职责、优先资质和真实经历证据。
4. 用户申请后主动索取官方 Posting URL，并记录可访问的 Job ID/JID 以排除重复申请。
5. 同机构同职位名称不自动判定为重复；类似 repost 只有证据足够才排除，边界情况单列复核。
6. 在用户要求时，由宿主为不同职位范围分别创建**定时计划任务**：仅新出现、仍开放、未申请且符合资格的优质岗位才提醒，或者按用户选择发送固定摘要。

### 网页端使用步骤
1. 交互调用 `SKILL.md` 获取搜索范围和匿名化经历（[模板](references/INTAKE_TEMPLATE.md)）。
2. 将[自包含的定时任务提示词](references/task-templates.md)填入 ChatGPT Scheduled Tasks 或 Muse 支持的目标/自动化任务。不同搜索条件建议建立不同任务。
3. 申请职位后更新同一个计划任务能够访问的 Applied Jobs 列表；不要假设其他聊天中的记录自动同步。
4. 用[验收场景](references/acceptance-scenarios.md)验证首次基线、重复岗位、官方关闭状态和无变化时的行为。

**注意：** 项目本身不能保证 ChatGPT 或 Muse 会直接安装/调用 GitHub Skill；定时执行及跨次结果访问取决于宿主。将完整规则和必要的匿名输入保留在任务自身的私有指令中。公开仓库不应包含候选人工作经历或申请记录。

## English

A **prompt-only, browser-agent Skill** for searching current official NYC CityJobs and matching real job descriptions to an anonymized candidate profile. Intended for ChatGPT Scheduled Tasks, Meta Muse and similar cloud agents; no local Python, crawler, database or hosted app required.

### Workflows
- **Explicit targets:** search strictly within the user's requested scope, any occupational domain.
- **Unknown targets:** infer supported role families from anonymized professional duties and credentials, then read actual vacancy JDs.
- **Specific JD:** assess mandatory eligibility, civil-service requirements, responsibilities and evidence; never inflate matches based on title/keywords.
- **Applied exclusions:** save official Job ID/JID/URL in the host's private task instructions or state; identical agency/title is **not** sufficient for auto-exclusion.
- **Scheduled monitoring:** create independent host tasks by user-selected scope/cadence; notify for verified newly open, qualified, unapplied opportunities or send selected digests.

### Start
Use `SKILL.md` interactively to obtain scope and anonymous input, then put the [standalone scheduled task prompt](references/task-templates.md) into the hosting platform. It works even without automatic `SKILL.md` loading. Keep private applied-job IDs in task-accessible state and update task instructions following each new application. If previous run state is unavailable, do not claim to know which jobs are newly posted. [Acceptance scenarios](references/acceptance-scenarios.md) cover expected behavior.

## Files
- `SKILL.md` — agent instructions.
- `references/INTAKE_TEMPLATE.md` — anonymized input.
- `references/STATE_SCHEMA.md` — **conceptual**, host-dependent private state.
- `references/task-templates.md` — standalone recurring task instructions.
- `references/acceptance-scenarios.md` — manual prompt-level evaluation cases.

**The host, not this repository, is responsible for scheduling, persistence and notifications.**
