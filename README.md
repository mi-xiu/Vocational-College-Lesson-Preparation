# 高职课程开发专家团 · gaohi-course-team

> **版本 v1.3.5** ｜ 类型：Team 型多角色协作专家团队 ｜ 作者：米修老师（mixstudio@qq.com）
> 适用平台：WorkBuddy 桌面版（专家注册于 `my-experts` marketplace）
> 配套文档：`专家团使用说明.md`（完整使用手册）、`版本号管理办法.md`（发版纪律）

[![Version](https://img.shields.io/badge/version-1.3.5-blue.svg)](./版本号管理办法.md)
[![Type](https://img.shields.io/badge/type-Team--Expert-green.svg)](./.codebuddy-plugin/plugin.json)
[![License](https://img.shields.io/badge/license-CC--BY--NC--4.0-lightgrey.svg)](#许可证)
[![Members](https://img.shields.io/badge/members-11%20agents-orange.svg)](./.codebuddy-plugin/plugin.json)

---

## 这是什么

「高职课程开发专家团」是一支由 **1 位主理人（课程总监）+ 10 位成员专家** 组成的 AI 协作团队，按 **三阶段 SOP** 把一门高职课程从「空盘」建到「可上课的备课包」。

团队严守高职课程建设的六条红线，覆盖从岗位调研、能力图谱、课程标准，到整体设计、单元设计、备课素材，再到 Office 文档统一出稿（docx/pptx）与教学平台对接（智慧职教）的**全流程**。它不是单个聊天机器人，而是一套**有主编排、有纪律、有分工**的课程建设流水线。

### 适用场景

| 你的诉求 | 触发话术示例 |
|---|---|
| 从零建设一门高职课的完整交付物 | 「按专家团三阶段流程，帮我从零建设一门高职课的完整交付物（课标/整体设计/单元/备课包）」 |
| 接手一门已开设课程，先做现状诊断 | 「我接手了一门已开设课程，先帮我做课程现状梳理（教材/学情/课时/项目来源/模板）」 |
| 课程要参赛，按岗课赛证重做课标与整体设计 | 「这门课要参赛，帮我按岗课赛证框架重做课标与整体设计」 |
| 把建好的课程成果对接到教学平台（如智慧职教） | 「把这门课的知识图谱按智慧职教规范补全并导出」 |

---

## 组织架构（11 位 Agent）

| 序 | 阶段 | 成员 ID | 名字 | 职责 | 包装技能 |
|---|---|---|---|---|---|
| 00 | 编排 | `gaozhi-course-team-lead` | 程督远（课程总监） | 编排调度、守红线、S20 收尾校验 | `ti-s01-s09-course-build` |
| 01 | 一 | `post-research` | 许岗清 | ① 岗位调研（S01） | `ti-s01-course-direction` |
| 02 | 一 | `competency-map` | 蒲图明 | ② 能力图谱（S02+S03） | `ti-s03-competency-map` + `ti-s02-task-resource` |
| 03 | 一 | `course-standard` | 柯标严 | ③ 课程标准（S04） | `ti-s04-course-standard` |
| 04 | 二 | `course-audit` | 甄况清 | ④ 课程现状梳理（S05） | `ti-s05-course-audit` |
| 05 | 二 | `course-blueprint` | 邵局周 | ⑤ 整体设计（S06+S08） | `ti-s06-course-blueprint` + `ti-s08-teaching-plan` |
| 06 | 三 | `unit-design` | 段元微 | ⑥ 单元设计（S07） | `ti-s07-unit-design` |
| 07 | 三 | `lesson-prep` | 贝资备 | ⑦ 备课素材（S09） | `ti-s09-lesson-prep` + `ti-s02-resource-collector` |
| 08 | 三 | `office-docs` | 台导出 | ⑧ 模板导出专家（v1.3.4，套用户/默认模板·格式零改动只换内容 + 单元教案通道） | `ti-office-docs` |
| 09 | 三 | `industry-advisor` | 行顾问 | ⑨ 行业知识顾问（v1.3.0） | `ti-industry-advisor` |
| 10 | 对接 | `ti10-teaching-platform` | 台对接 | ⑩ 教学平台路由（v1.3.2，智慧职教等） | `Ti_图谱4智慧职教` |

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
gaozhi-course-team/
├── .codebuddy-plugin/
│   └── plugin.json              # 团队包元数据（name/version/members/displayName…）
├── README.md                    # 本说明（GitHub 主页）
├── LICENSE                      # CC BY-NC 4.0 许可证全文
├── .gitignore                   # Git 忽略规则（OS / Python / Node / 构建产物）
├── CONTRIBUTING.md              # 贡献与二次开发指南
├── 专家团使用说明.md            # 完整使用手册（安装/调用/工作流/红线/注意事项）
├── 版本号管理办法.md            # 发版纪律（按发布范围定版本级别）
├── 分享操作指引.md              # 历史分享操作说明
├── agents/                      # 11 个 agent 定义（lead + 10 成员）
├── skills/                      # 14 个包装技能（见上表"包装技能"列）
├── templates/
│   └── 默认输出三件套/           # 课程标准 / 授课计划 / 单元教案 三套 spec（Ti08 格式真源）
├── knowledge/                   # 共享知识库（纯 md）
│   ├── A01-上级文件/            # 教育强国建设规划纲要、教职成〔2026〕1号文（md）
│   ├── A02-专家资料/            # 从岗位到课堂（十五五规划教材编写实战，md）
│   ├── 行业库/                  # film 影视行业库（默认加载）+ _模板 + README
│   └── 教职成〔2026〕1号文解读与课程建设落地对照（充实版）.md
├── avatars/                     # 11 张成员头像（512×512，程序化生成）
└── style_lib/                   # 文档风格库
```

> **关于 PDF**：v1.3.5 起知识库已**纯 md 化**——原 3 份政策 PDF（纲要 / 1号文 / 从岗位到课堂）已完整转写为 md 并移除原件，日常检索与引用统一走 md，无二进制依赖。

---

## 快速开始

### 方式 A · 放入 WorkBuddy 专家目录（推荐开发者）

```bash
git clone <本仓库地址> gaohi-course-team
# macOS / Linux
cp -r gaohi-course-team ~/.workbuddy/plugins/marketplaces/my-experts/plugins/
# Windows（PowerShell）
Copy-Item -Recurse gaohi-course-team "$env:USERPROFILE\.workbuddy\plugins\marketplaces\my-experts\plugins\"
```

放入后重启 WorkBuddy，在「专家」入口即可看到 **高职课程开发专家团（v1.3.5·含教学平台）**。

### 方式 B · 离线 `.wbp` 安装（普通用户）

从 GitHub Releases 下载随版发布的 `高职课程开发专家团_v1.3.5.wbp`（或 `.zip`），双击即可离线安装整团（Mac/Windows 通用，无需联网/账号）。团队包已内嵌全部 11 位专家副本，无需逐个安装。

### 调用

在 WorkBuddy 选择该专家团，直接说出诉求即可（见上方「适用场景」触发话术）。课程总监会自动按三阶段 SOP 调度成员、守红线、做 S20 校验。

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

规则与升级判级（**按发布范围而非功能大小**）、四字段带版本号纪律、嵌入副本同步流程与 Changelog，见 **[版本号管理办法.md](./版本号管理办法.md)**。

### Changelog

- **v1.3.5（2026-09-19）**：知识库纯 md 化——`knowledge/` 三份政策 PDF（纲要 / 1号文 / 从岗位到课堂）全部转写为 md 并移除原件，日常检索/引用统一走 md，无二进制依赖；`README.md` 更新时间同步。
- **v1.3.4（2026-08-20）**：⑧ 号成员 **Ti08 模板导出专家** 把"单元教案导出逻辑"从单课程项目脚本提升为**技能级通用通道**（`ti-office-docs/scripts/unit-lesson-plan/`：engine.py 段落引擎 + unit_channel.py 运行器 + 单元教案-fieldmap.json 模板映射），与课程解耦；`verify_faith.py` 段落校验改为"签名子集"判定；明确 S07→Ux 路由触发。
- **v1.3.3（2026-08-20）**：⑧ 号成员 **office-docs 改名「Ti08 模板导出专家」**。核心转变：以用户/默认模板为唯一格式真源，**格式零改动、只替换内容**；默认输出模板固化为**三件套**（课程标准/授课计划/单元教案）；新增模板规范化门与保真核对。
- **v1.3.2（2026-08）**：新增 ⑩ 号成员 **Ti10 教学平台专家**，负责把课程成果按目标平台路由到对应平台子技能；当前接入智慧职教（含知识图谱属性填充）。
- **v1.3.1**：Ti08 并入「学校官方模板保真管线」——optimize/render/verify 三件套 + course.yaml 单一真源 + build_course 编排器。
- **v1.3.0**：新增 Ti09 行业知识顾问；内置 S20 终校、docx 批量转换、W1 PPT 自动生成、单元对齐注入等自动化脚本。

---

## 许可证

本专家团以 **CC BY-NC 4.0（署名-非商业性使用）** 发布：可自由学习、二次开发、在教研场景内部使用，但**不得用于商业售卖或闭源封装**；二次发布请保留作者署名（米修老师）与版本号。

> 如需其他授权（如商业授权、纳入机构私有分发），请联系作者 mixstudio@qq.com。

## 二次开发

可基于本包增减成员/技能；改动后按《版本号管理办法.md》bump 版本号，并将团队包重新打包为带版本号的 `.zip`/`.wbp`（见各 Release 资产）后发布。

## 致谢

知识库政策口径以教职成〔2026〕1号文、教育强国建设规划纲要（2024—2035年）及《从岗位到课堂》教材编写实战路径为准；行业库默认加载影视行业（film），可按 `knowledge/行业库/_模板/` 扩展其他专业。
