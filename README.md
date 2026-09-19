# 职教课程开发专家团 · vocational-college-lesson-preparation

## 适用于所有面向职业岗位的课程开发

**与专业无关、与课程无关** —— 本团适用于**所有面向职业岗位的课程开发**：中等职业教育 · 高职专科 · 职业本科，覆盖装备制造、电子信息、财经商贸、医药卫生、文化艺术、交通运输、教育与体育、农林牧渔、旅游、公共管理与服务等**全部专业大类**。无论你教的是《微电影编导》还是《数控加工工艺》，团队走的是同一条链路。

通用的机制只有两句话：

> **换专业不改团队，只换 industry-libs** —— `knowledge/industry-libs/` 可插拔（默认 `film`），换专业只需建一份该专业的 industry-libs
> **换学校不改团队，只换模板** —— 以你学校的模板为唯一格式真源，格式零改动、只替换内容

---

> **版本 v1.5.0** ｜ 类型：Team 型多角色协作专家团队 ｜ 作者：米修老师（mixstudio@qq.com）
> 适用平台：WorkBuddy 桌面版（专家注册于 `my-experts` marketplace）
> 适用范围：中职 / 高职专科 / 职业本科 · 全专业大类通用
> 配套文档：`USAGE.md`（完整使用手册）、`VERSIONING.md`（发版纪律）

[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](./VERSIONING.md)
[![Type](https://img.shields.io/badge/type-Team--Expert-green.svg)](./.codebuddy-plugin/plugin.json)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#许可证)
[![Members](https://img.shields.io/badge/members-11%20agents-orange.svg)](./.codebuddy-plugin/plugin.json)

---

## 这是什么

「职教课程开发专家团」是一支由 **1 位主理人（课程总监）+ 10 位成员专家** 组成的 AI 协作团队，按 **三阶段 SOP** 把一门**职业教育课程**从「空盘」建到「可上课的备课包」。

**它是通用的：与专业无关、与课程无关。** 同一套流水线可用于任意专业大类的职业教育课程开发——装备制造、电子信息、财经商贸、医药卫生、文化艺术、交通运输、教育与体育、农林牧渔、旅游、公共管理与服务……无论你教的是《微电影编导》还是《数控加工工艺》，团队走的是同一条链路，产出的课标、整体设计、单元教案、备课包全部围绕**你指定的岗位与学校模板**生成。

团队严守职教课程建设的六条红线，覆盖从岗位调研、能力图谱、课程标准，到整体设计、单元设计、备课素材，再到 Office 文档统一出稿（docx/pptx）与教学平台对接（智慧职教）的**全流程**。它不是单个聊天机器人，而是一套**有主编排、有纪律、有分工**的课程建设流水线。

### 适用对象

| 维度 | 覆盖范围 |
|---|---|
| **教育层次** | 中等职业教育 · 高职专科 · 职业本科（含应用型本科的课程改造） |
| **专业大类** | **全大类通用**——装备制造、电子信息、财经商贸、医药卫生、文化艺术、交通运输、教育与体育、农林牧渔、旅游、公共管理与服务等 |
| **课程性质** | 专业课 · 专业基础课 · 实训课 · 微专业 / 1+X 证书课 · 岗课赛证融通改造课 |
| **建设阶段** | 新建课程（从零） · 存量课程改造 · 参赛打磨 · 教材申报 · 教学平台对接 |
| **使用者** | 任课教师 · 教研室 / 专业负责人 · 课程建设团队 · 教学设计师 |

### 通用性：为什么任何一门职教课都能用

团队把课程开发的三件事彻底分开，**只有中间一层随专业变化**：

| 层 | 是否随专业变化 | 说明 |
|---|---|---|
| ① **方法论层**（PGSD 四维 + 三阶段 SOP + 六条红线） | ❌ 完全不变 | 岗位调研 → 能力图谱 → 课标 → 整体设计 → 单元设计 → 备课包，任何专业都走同一条链路；P/G/S/D 能力编号、课标与整体设计两层分离等红线对所有课程一视同仁 |
| ② **行业知识层**（`knowledge/industry-libs/` 可插拔） | ✅ 随专业切换 | 默认加载 `film` 影视 industry-libs；换专业只需按 `industry-libs/_template/` 建一份新库（岗位清单 / 典型任务 / 案例台账 / 工艺方法），团队即可产出该专业的专业内容 |
| ③ **文档格式层**（学校模板为唯一真源） | ✅ 随学校变化 | Ti08 模板导出专家以**你学校的模板**为唯一格式真源，**格式零改动、只替换内容**；换成哪家学校的模板，输出就是哪家的格式 |

一句话：**换专业不改团队，只换 industry-libs；换学校不改团队，只换模板。** 课程名、专业、学时 / 周次、项目载体等，在启动对话时作为参数直接给出即可。

### 适用场景

| 你的诉求 | 触发话术示例 |
|---|---|
| 从零建设一门职教课的完整交付物（**任意专业**） | 「按专家团三阶段流程，帮我从零建设《XX 课》的完整交付物（课标/整体设计/单元/备课包），专业是 XX，56 学时 14 周」 |
| 接手一门已开设课程，先做现状诊断 | 「我接手了一门已开设课程，先帮我做课程现状梳理（教材/学情/课时/项目来源/模板）」 |
| 课程要参赛，按岗课赛证重做课标与整体设计 | 「这门课要参赛，帮我按岗课赛证框架重做课标与整体设计」 |
| 把建好的课程成果对接到教学平台（如智慧职教） | 「把这门课的知识图谱按智慧职教规范补全并导出」 |
| 切换到非默认行业（如机电、护理、电商） | 「我要建的是机电/护理/电商课，先在 `knowledge/industry-libs/` 下建一份该专业的 industry-libs，再按三阶段流程建课」 |
| 按本校模板出稿 | 「我们学校有自己的课标/授课计划/教案模板，按本校模板导出，格式不要动」 |

---

## 组织架构（11 位 Agent）

| 序 | 阶段 | 成员 ID | 名字 | 职责 | 包装技能 |
|---|---|---|---|---|---|
| 00 | 编排 | `vocational-college-lesson-preparation-lead` | 程督远（课程总监） | 编排调度、守红线、S20 收尾校验 | `ti-s01-s09-course-build` |
| 01 | 一 | `post-research` | 许岗清 | ① 岗位调研（S01） | `ti-s01-course-direction` |
| 02 | 一 | `competency-map` | 蒲图明 | ② 能力图谱（S02+S03） | `ti-s03-competency-map` + `ti-s02-task-resource` |
| 03 | 一 | `course-standard` | 柯标严 | ③ 课程标准（S04） | `ti-s04-course-standard` |
| 04 | 二 | `course-audit` | 甄况清 | ④ 课程现状梳理（S05） | `ti-s05-course-audit` |
| 05 | 二 | `course-blueprint` | 邵局周 | ⑤ 整体设计（S06+S08） | `ti-s06-course-blueprint` + `ti-s08-teaching-plan` |
| 06 | 三 | `unit-design` | 段元微 | ⑥ 单元设计（S07） | `ti-s07-unit-design` |
| 07 | 三 | `lesson-prep` | 贝资备 | ⑦ 备课素材（S09） | `ti-s09-lesson-prep` + `ti-s02-resource-collector` |
| 08 | 三 | `office-docs` | 台导出 | ⑧ 模板导出专家（v1.3.4，套用户/默认模板·格式零改动只换内容 + 单元教案通道） | `ti-office-docs` |
| 09 | 三 | `industry-advisor` | 行顾问 | ⑨ 行业知识顾问（v1.3.0，**industry-libs 可插拔**，默认 film） | `ti-industry-advisor` |
| 10 | 对接 | `ti10-teaching-platform` | 台对接 | ⑩ 教学平台路由（v1.3.2，智慧职教等） | `ti-zhihui-zhijiao-graph` |

> **MBTI ↔ 角色固定映射**（头像纪律）：lead=ENTJ / post-research=ESTJ / competency-map=INTJ / course-standard=ISTJ / course-audit=ISTP / course-blueprint=ENTP / unit-design=ISFJ / lesson-prep=ESTP。头像统一内置 `avatars/`（512×512），程序化生成、纯人像无文字，遵守红线第 6 条。

### 三阶段 SOP（协作时序）

```
阶段一（串行 · 职业分析与标准）
  ① 岗位调研 ──▶ ② 能力图谱 ──▶ ③ 课程标准
        │
阶段二（可并行 · 现状诊断与落地设计）
  ④ 课程现状梳理 （可并行于阶段一早期）
  ⑤ 整体设计
        │
阶段三（串行 · 教学开发与备课）
  ⑥ 单元设计 ──▶ ⑦ 备课素材 ──▶ ⑧ Office 文档出稿
        │                └─ ⑨ 行业知识顾问（全程供给，不单独成阶段）
        │
  ── ⑩ 教学平台路由（成果对接维度，松耦合接入）──
        │
  S20 收尾校验（由课程总监统一兜底）
```

**调度铁律**：团队创建只能由课程总监执行；成员独立产出，结论以对应成员输出为准；成员间不直连，产出经课程总监中转、汇编、转交下一阶段。

---

## 目录结构（本仓库实际内容）

```
vocational-college-lesson-preparation/
├── .codebuddy-plugin/
│   └── plugin.json              # 团队包元数据（name/version/members/displayName…）
├── README.md                    # 本说明（GitHub 主页）
├── LICENSE                      # MIT 许可证全文
├── .gitignore                   # Git 忽略规则（OS / Python / Node / 构建产物）
├── CONTRIBUTING.md              # 贡献与二次开发指南
├── USAGE.md            # 完整使用手册（安装/调用/工作流/红线/注意事项）
├── VERSIONING.md            # 发版纪律（按发布范围定版本级别）
├── SHARING.md              # 历史分享操作说明
├── agents/                      # 11 个 agent 定义（lead + 10 成员）
├── skills/                      # 14 个包装技能（见上表"包装技能"列）
├── templates/
│   └── default-output-trio/           # 课程标准 / 授课计划 / 单元教案 三套 spec（Ti08 格式真源）
├── knowledge/                   # 共享知识库（纯 md）
│   ├── A01-authority-docs/            # 教育强国建设规划纲要、教职成〔2026〕1号文（md）
│   ├── A02-expert-materials/            # 从岗位到课堂（十五五规划教材编写实战，md）
│   ├── industry-libs/                  # 可插拔行业知识库：film 影视库（默认加载）+ _template（扩展新专业）+ README
│   └── A01-03-no1-doc-interpretation-and-course-alignment.md
├── avatars/                     # 11 张成员头像（512×512，程序化生成）
└── style_lib/                   # 文档风格库
```

> **关于 PDF**：v1.3.5 起知识库已**纯 md 化**——原 3 份政策 PDF（纲要 / 1号文 / 从岗位到课堂）已完整转写为 md 并移除原件，日常检索与引用统一走 md，无二进制依赖。

---

## 快速开始

### 方式 A · 放入 WorkBuddy 专家目录（推荐开发者）

```bash
git clone <本仓库地址> vocational-college-lesson-preparation
# macOS / Linux
cp -r vocational-college-lesson-preparation ~/.workbuddy/plugins/marketplaces/my-experts/plugins/
# Windows（PowerShell）
Copy-Item -Recurse vocational-college-lesson-preparation "$env:USERPROFILE\.workbuddy\plugins\marketplaces\my-experts\plugins\"
```

放入后重启 WorkBuddy，在「专家」入口即可看到 **职教课程开发专家团（v1.5.0·全专业通用·含教学平台）**。

### 方式 B · 离线 `.wbp` 安装（普通用户）

从 GitHub Releases 下载随版发布的 `vocational-college-lesson-preparation-v1.5.0.wbp`（或 `.zip`），双击即可离线安装整团（Mac/Windows 通用，无需联网/账号）。团队包已内嵌全部 11 位专家副本，无需逐个安装。

> 说明：GitHub Release **资产名不支持中文**，故线上资产用 ASCII 名 `vocational-college-lesson-preparation-v1.5.0.zip` / `.wbp`；本地同名中文文件 `职教课程开发专家团_v1.5.0.zip` 与之字节级一致，二者是同一个包。

### 调用

在 WorkBuddy 选择该专家团，直接说出诉求即可（见上方「适用场景」触发话术）。课程总监会自动按三阶段 SOP 调度成员、守红线、做 S20 校验。

**启动时建议一次说清这几个参数**（越具体，产出越贴合；专业不限）：

| 参数 | 示例 |
|---|---|
| 课程名称 | 《微电影编导》 |
| 专业与层次 | 传播与策划专业 · 高职专科大二 |
| 学时 / 周次 | 56 学时 = 4 学时 × 14 周 |
| 区域产业基准（可选） | 浙江 / 杭州广告与新媒体产业集群 |
| industry-libs | 默认 `film`；其他专业请指定或先建库 |
| 学校模板（可选） | 提供本校课标 / 授课计划 / 教案模板，出稿时格式零改动 |

> 不给全也能跑——缺失项由团队按行业基准与政策口径兜底假设，并在产出中标注，供你确认后回环修正。

---

## 六条红线（全团 MUST，课程总监统一兜底）

1. **PGSD 编号统一**：能力点全程沿用 P/G/S/D 四维与既有编号，下游不得另起一套。
2. **课标·整体设计两层分离**：课标只到模块、不绑周次；整体设计绑定项目/作品/周次；两文件并列不混写。
3. **命名纪律**：`<课程名>-课程标准.md` / `<课程名>-课程整体设计（<项目版>）.md`。
4. **禁特定证书体系**：证书口径统一「证书 / 职业技能等级证书 / 行业认证 / 企业认证」。
5. **量规二值 + ★ 闸门**：评价判定用 ✔/✘ + ★ 闸门，不套 4 级量表（学校官方模板自身用百分制时以学校模板为准）。
6. **头像纪律**：只用纯人像无文字图；MBTI↔角色固定映射（见组织架构表）。

---

## 版本管理

规则与升级判级（**按发布范围而非功能大小**）、四字段带版本号纪律、嵌入副本同步流程与 Changelog，见 **[VERSIONING.md](./VERSIONING.md)**。

### Changelog

- **v1.5.0（2026-09-19）**：**11 位成员头像按人格测试（MBTI）统一重制**——原头像为混搭风格（10 张 3D 低多边形 + 1 张写实照片）且与人格类型无视觉关联，本次全部重制为统一的 3D 低多边形风（512×512、纯人像无水印无边框），并按 **16personalities 族群配色**分区：分析家 NT=紫（lead / competency-map / course-blueprint）、外交家 NF=绿（industry-advisor）、守护者 SJ=蓝（post-research / course-standard / unit-design / office-docs）、探索者 SP=黄（course-audit / lesson-prep / ti10）。红线第六条**补齐 Ti08=ESFJ / Ti09=ENFJ / Ti10=ESFP** 三位成员的 MBTI 映射；修复 `ti10-teaching-platform.png` 与 lead 头像**共用同一张图**（md5 相同）的重复缺陷。按「全体发版」判级 **Y+1**。
- **v1.4.0（2026-09-19）**：**品牌与标识统一更名**——中文名「高职课程开发专家团」→「**职教课程开发专家团**」，插件 ID / 目录名 `gaozhi-course-team` → `vocational-college-lesson-preparation`（与 GitHub 仓库同名，全小写 + 连字符），lead agent 与头像同步改名；**仓库内文件名全量 ASCII 化**（`knowledge/` 政策文件、`templates/` 三件套与 L0–L3 模板、单元教案/课程标准/授课计划模板、根目录 `USAGE.md` / `SHARING.md` / `VERSIONING.md`、技能目录 `ti-zhihui-zhijiao-graph`），发布资产不再因中文名被 GitHub 剔字；正文「高职」按语义区分：品牌义改「职教」，层次义（高职专科 / 中职 / 高职院校）保留。团队能力未变，本次为**标识与命名层修订**，按「全体发版」判级 Y+1。
- **v1.3.6（2026-09-19）**：**明确通用定位**——README 顶部写明「适用于所有面向职业岗位的课程开发（中职 / 高职专科 / 职业本科 · 全专业大类）」，并给出通用机制「换专业不改团队只换 industry-libs，换学校不改团队只换模板」；新增「适用对象」表与「通用性三层解耦」表（方法论层不变 / 行业知识层可插拔 / 文档格式层以学校模板为真源）；补充启动参数表与「扩展到其他专业」步骤；`plugin.json` 四字段、默认提示语同步通用化。团队能力未变，为**定位与文档层修订**。
- **v1.3.5（2026-09-19）**：知识库纯 md 化——`knowledge/` 三份政策 PDF（纲要 / 1号文 / 从岗位到课堂）全部转写为 md 并移除原件，日常检索/引用统一走 md，无二进制依赖；`README.md` 更新时间同步。
- **v1.3.4（2026-08-20）**：⑧ 号成员 **Ti08 模板导出专家** 把"单元教案导出逻辑"从单课程项目脚本提升为**技能级通用通道**（`ti-office-docs/scripts/unit-lesson-plan/`：engine.py 段落引擎 + unit_channel.py 运行器 + unit-lesson-plan-fieldmap.json 模板映射），与课程解耦；`verify_faith.py` 段落校验改为"签名子集"判定；明确 S07→Ux 路由触发。
- **v1.3.3（2026-08-20）**：⑧ 号成员 **office-docs 改名「Ti08 模板导出专家」**。核心转变：以用户/默认模板为唯一格式真源，**格式零改动、只替换内容**；默认输出模板固化为**三件套**（课程标准/授课计划/单元教案）；新增模板规范化门与保真核对。
- **v1.3.2（2026-08）**：新增 ⑩ 号成员 **Ti10 教学平台专家**，负责把课程成果按目标平台路由到对应平台子技能；当前接入智慧职教（含知识图谱属性填充）。
- **v1.3.1**：Ti08 并入「学校官方模板保真管线」——optimize/render/verify 三件套 + course.yaml 单一真源 + build_course 编排器。
- **v1.3.0**：新增 Ti09 行业知识顾问；内置 S20 终校、docx 批量转换、W1 PPT 自动生成、单元对齐注入等自动化脚本。

---

## 许可证

本专家团以 **MIT License** 发布：可自由使用、复制、修改、合并、出版、分发、再许可与销售，包括商用与闭源二次分发，**唯一条件是保留本许可证全文与作者署名**（米修老师）。

> 软件按「原样」提供，作者不承担任何明示或暗示的担保责任。如需定制开发或商业合作，请联系 mixstudio@qq.com。

## 二次开发

可基于本包增减成员/技能；改动后按《VERSIONING.md》bump 版本号，并将团队包重新打包为带版本号的 `.zip`/`.wbp`（见各 Release 资产）后发布。

## 扩展到其他专业

本包开箱带 `film`（影视） industry-libs，但**不限于影视**。把团队用于你自己的专业，只需两步：

1. 复制 `knowledge/industry-libs/_template/`，建一份你专业的 industry-libs （岗位清单 / 典型工作任务 / 案例台账 / 工艺方法 / 证书与竞赛口径）；
2. 启动时指定你的课程参数（课程名 / 专业 / 学时周次 / 区域产业基准）。

方法论层与红线无需任何改动即可复用。欢迎把你建好的 industry-libs PR 回来（见 `CONTRIBUTING.md`），一起把覆盖面扩到更多专业大类。

## 致谢

知识库政策口径以教职成〔2026〕1号文、教育强国建设规划纲要（2024—2035年）及《从岗位到课堂》教材编写实战路径为准； industry-libs 默认加载影视行业（film），可按 `knowledge/industry-libs/_template/` 扩展其他专业，使本团适用于全部职业教育专业大类的课程开发。
