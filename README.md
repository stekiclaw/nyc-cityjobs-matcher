# NYC CityJobs Matcher Skill

[中文](#中文) · [English](#english)

## 中文

一个可复用、注重隐私的 Skill，用于将 NYC CityJobs 的招聘岗位与匿名化的候选人经历进行匹配。

### 核心功能

1. 首次进行个性化匹配时，主动要求用户提供匿名化的工作经历。
2. 明确提示：不要提供个人工作经历中的雇主、公司、机构名称或任何人名。
3. 查询当前 NYC CityJobs 官方招聘信息，按照技能、职责、工作规模、成果、资质、公务员任用资格和个人偏好评估匹配程度。
4. 用户表示已申请岗位时，如未提供官方职位链接，主动索取该链接。
5. 从链接提取 Job ID、JID 和招聘信息，将岗位加入已申请岗位记录（Applied Jobs Ledger）。
6. 在后续推荐中排除已申请岗位及实质相同的重新发布岗位。
7. 提供真实的简历调整建议，不编造经验或资质。

### 搜索范围与结果

不预设 IT、技术标签或任何固定职业范围，搜索方式由用户需求决定：

- **已明确目标：** 按用户指定的职位、职责、关键词、机构和限制搜索。
- **不确定目标：** 根据匿名化工作经历、技能、成果、学历和执照判断适合的职位方向，再查找并逐条匹配招聘 JD。
- **已有职位链接或 JD：** 直接对照用户经历分析该岗位是否适合，无需先指定职位类别。

用户明确的搜索范围优先；经历用于判断范围内每条 JD 的匹配度。其他可能适合的方向会单独建议，不会擅自改变搜索范围。

逐条对照 JD 的必要资格、核心职责和优先条件，标明已有证据、部分符合、缺失或未知；不只比较职位名称或标签。推荐结果包括官方申请链接、机构、职位编号、薪资、发布日期和截止日期、任用资格、匹配理由、缺口及可能的硬性限制。对适合的岗位提供简历调整建议，并标记未来 14 天内的截止日期。

每次搜索使用最新资料，第三方信息仅用于发现线索，推荐前以官方招聘信息核实。已关闭的岗位不应作为可申请职位推荐。

### 安装与使用

将整个仓库作为 `nyc-cityjobs-matcher` 文件夹安装到支持 `SKILL.md` 的助手环境，并按照该环境的 Skills 安装流程启用。

示例：

```text
$nyc-cityjobs-matcher
根据我的匿名化工作经历，帮我寻找仍开放且匹配度高的 NYC 岗位，并排除我已申请的职位。
```

匿名化经历可以包含：

- 岗位类型、职责和大致工作年限。
- 专业技能、方法、工具、领域知识和工作规模。
- 可量化成果、证书和学历。
- 公务员 title、考试或名单资格（自愿提供）。
- 薪资、地点、通勤和办公方式偏好。

不要提供雇主或人名、联系方式、员工编号、内部主机名、私有链接、账号或凭据。无需上传完整简历，简短要点即可。公开招聘信息中的机构名称可出现在结果及申请记录中。

如果不提供经历，仍可进行一般职位搜索，但结果不能标为个性化匹配排名。

### 已申请岗位排除

申请后，将官方 NYC CityJobs 职位链接提供给助手。Skill 会使用 Job ID、JID、官方 URL、机构与职位信息识别岗位，并排除实质相同的重新发布记录。

如果暂时没有链接，可以在当前对话中临时排除明确指出的职位；持久去重仍需要官方链接。对疑似但无法确认相同的重新发布岗位，说明不确定性，避免误删不同机会。

### 文件结构

- `SKILL.md`：主要执行指令。
- `references/INTAKE_TEMPLATE.md`：匿名化经历收集模板。
- `references/STATE_SCHEMA.md`：候选人资料和已申请岗位记录的逻辑结构。

### 状态保存说明

Skill 定义匹配流程和状态结构，实际持久保存取决于运行环境。支持用户／Skill 状态时，将匿名化资料和已申请岗位记录保存在该环境中。否则只在当前对话中维护，切换环境时需要用户提供或导出记录。

仅安装 Skill 不会自动创建定时任务，也不能保证跨环境保留申请记录。不要将个人资料或申请记录提交到此公开仓库。

## English

A reusable, privacy-preserving skill for matching NYC CityJobs vacancies against an anonymized candidate profile.

### Core behavior

1. On first personalized use, asks the user for anonymized work experience.
2. Explicitly tells the user not to provide employer, company or agency names from their own work history, or people's names.
3. Searches current official NYC CityJobs listings and ranks fit using skills, responsibilities, scale, achievements, credentials, civil-service eligibility and preferences.
4. When the user says they applied to a job, requests the official job-posting URL if it was not supplied.
5. Extracts Job ID, JID and posting metadata from the link and adds the vacancy to an Applied Jobs Ledger.
6. Excludes the applied vacancy and materially identical reposts from future recommendations.
7. Provides truthful resume-tailoring notes without inventing experience or qualifications.

### Search scope and results

No IT focus, technology tags or fixed occupation list is imposed. The search follows the user's needs:

- **Known targets:** Search the roles, duties, keywords, agencies and constraints specified by the user.
- **Unknown targets:** Infer suitable role families from anonymized experience, skills, achievements, education and licenses, then search and assess each posting's JD.
- **An existing posting or JD:** Compare it directly with the user's experience without requiring a role family first.

Explicit scope controls where to search; experience determines how well each JD fits. Other suitable directions are offered separately rather than silently changing the scope.

Each JD is compared with the profile's evidence, separating mandatory qualifications, essential duties and preferred qualifications. Material requirements are marked as supported, partially supported, missing or unknown; titles and tags alone do not establish fit. Recommendations include official application links, agencies, job identifiers, salaries, posting and closing dates, civil-service eligibility, fit explanations, gaps and potential disqualifiers. Suitable roles receive resume-tailoring suggestions, and deadlines within 14 days are flagged.

Every search uses fresh research. Third-party information is for discovery only; recommendations are verified against official postings. Closed vacancies should not be presented as actionable opportunities.

### Installation and use

Install the entire repository as a folder named `nyc-cityjobs-matcher` in an assistant environment that supports `SKILL.md`, following that host's skill installation procedure.

Example:

```text
$nyc-cityjobs-matcher
Find high-fit NYC vacancies that are still open using my anonymized work experience, and exclude jobs I have already applied to.
```

An anonymized profile can include:

- Role types, responsibilities and approximate years of experience.
- Professional skills, methods, tools, domain knowledge and work scope.
- Quantified achievements, certifications and education.
- Civil-service title, exam or list eligibility, optionally.
- Salary, location, commute and work-arrangement preferences.

Do not provide employer or person names, contact details, employee IDs, internal hostnames, private URLs, account information or credentials. A complete resume is not required; a short bullet summary is sufficient. Public agency names from job postings may appear in results and the application ledger.

If the user declines to provide a profile, the skill can perform a general search, but it must not describe the results as a personalized fit ranking.

### Applied-job exclusions

After applying, give the assistant the official NYC CityJobs posting link. The skill uses Job ID, JID, canonical URL, agency and vacancy details to identify the job and exclude materially identical reposts.

Without a link, an explicitly identified job can be temporarily suppressed in the current conversation. Durable deduplication still requires the official posting URL. Borderline reposts should be labeled as uncertain rather than silently excluding a potentially different vacancy.

### Package structure

- `SKILL.md`: Main skill instructions.
- `references/INTAKE_TEMPLATE.md`: Privacy-preserving experience intake.
- `references/STATE_SCHEMA.md`: Logical schema for the anonymized profile and Applied Jobs Ledger.

### Persistence

The skill defines behavior and a state model; actual persistence depends on the host. If the host supports skill or user state, store the normalized profile and Applied Jobs Ledger there. Otherwise, maintain them in the active conversation and ask the user to provide or export the ledger when moving to a new environment.

Installing the skill does not create a scheduled task or guarantee that application history transfers between environments. Do not commit personal profiles or application ledgers to this public repository.
