#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""创建高职课程建设工作区骨架（对齐 K02 权威结构：00–08 + 99）。

替代旧版「扁平 01–09 草案」骨架。

用法示例：
    python3 create_workspace.py \
        --root ~/WorkBuddy \
        --course-name "直播电商" \
        --code K03 \
        --direction "直播电商·内容运营" \
        --weeks 14

设计原则：
  1) 结构对齐高职课程建设标准目录（四阶段 00–08 + 99）。
  2) 幂等且安全：目录 exist_ok；文件默认 **不覆盖**（呼应"回退不删原文件"纪律），
     需覆盖时显式传 --overwrite。可反复重跑补齐缺失目录。
  3) 只建骨架 + 轻量占位，正文由 S01–S09 逐步经审批门填充。
  4) 不创建 .workbuddy/（由 WorkBuddy 自动生成）。
"""

from __future__ import annotations

import argparse
from pathlib import Path

# ========================= 一、结构常量 =========================

# 顶层目录：(基础名, 步骤标注后缀, 用途说明)
# 注：K02 磁盘实际不带括号后缀，后缀仅用于文档注记；--annotate-steps 可加回目录名。
TOP_DIRS = [
    ("00_参考资料",          "",             "共享：平台指南 · 行业标准 · 备课教程"),
    ("01_工作调研与课程标准", "（S01–S04）",  "职业分析 → 典型任务 → 能力图谱 → 课程标准"),
    ("02_教学资源",          "",             "共享池：案例库 · 建设工具包 · 教材与学材"),
    ("03_学情与整体设计",     "（S05·S06）",  "学生画像 + 课程整体设计"),
    ("04_单元教学设计",       "（S07）",      "逐周单元设计 + 总览"),
    ("05_课堂备课包",         "（S08）",      "10 子步反向设计备课包"),
    ("06_课程实施",           "（S09·实施）", "授课实录 · 实训指导 · 学生作品"),
    ("07_优化与运维",         "（S09·改进）", "反馈与改进 · 版本迭代 · 建设总结"),
    ("08_申报与成果",         "",             "申报 · 获奖 · 论文 · 历史版本"),
    ("99_工程与脚本",         "",             "一次性脚本归档"),
]

# 各顶层目录下的固定子目录（相对路径，可多级）
SUB_DIRS = {
    "01_工作调研与课程标准": [
        "S01_职业分析与就业调研",
        "S02_典型工作任务分析（含案例台账）",
        "S02_典型工作任务分析（含案例台账）/案例台账",
        "S03_能力图谱与技能点（PGSD）",
        "S04_课程标准",
    ],
    "02_教学资源": ["案例库/cases", "建设工具包", "教材与学材"],
    "03_学情与整体设计": [
        "S05_学生画像与学情",
        "S06_课程整体设计",
        "S06_课程整体设计/作品级教学设计",
    ],
    "05_课堂备课包": ["说明与规格", "数字化资源/脚本清单", "考核评价"],
    "06_课程实施": ["授课实录", "实训指导", "学生作品"],
    "07_优化与运维": ["反馈与改进", "版本迭代", "建设总结"],
    "08_申报与成果": ["历史版本"],
    "99_工程与脚本": ["一次性脚本"],
}

# 备课包内子目录：00_本包说明 为包头，01–10 对应 S08-1…S08-10
PKG_SUBDIRS = [
    "00_本包说明", "01_工作页", "02_考题", "03_量规", "04_学材", "05_讲稿",
    "06_PPT", "07_动画", "08_微课", "09_设备耗材安全", "10_拓展分层",
]

# 18 步清单：(编号, 名称, 进度表中的默认落点)
STEPS = [
    ("S01", "职业分析与就业调研", "01_工作调研与课程标准/S01_职业分析与就业调研/"),
    ("S02", "典型工作任务分析（含案例台账）", "01_工作调研与课程标准/S02_典型工作任务分析（含案例台账）/"),
    ("S03", "能力图谱与技能点（PGSD）", "01_工作调研与课程标准/S03_能力图谱与技能点（PGSD）/"),
    ("S04", "课程标准", "01_工作调研与课程标准/S04_课程标准/"),
    ("S05", "学生画像与学情", "03_学情与整体设计/S05_学生画像与学情/"),
    ("S06", "课程整体设计", "03_学情与整体设计/S06_课程整体设计/"),
    ("S07", "单元设计", "04_单元教学设计/"),
    ("S08-1", "工作页", "05_课堂备课包/<周包>/01_工作页/"),
    ("S08-2", "考题", "05_课堂备课包/<周包>/02_考题/"),
    ("S08-3", "量规", "05_课堂备课包/<周包>/03_量规/"),
    ("S08-4", "学材", "05_课堂备课包/<周包>/04_学材/"),
    ("S08-5", "讲稿", "05_课堂备课包/<周包>/05_讲稿/"),
    ("S08-6", "PPT", "05_课堂备课包/<周包>/06_PPT/"),
    ("S08-7", "动画", "05_课堂备课包/<周包>/07_动画/"),
    ("S08-8", "微课", "05_课堂备课包/<周包>/08_微课/"),
    ("S08-9", "设备耗材安全", "05_课堂备课包/<周包>/09_设备耗材安全/"),
    ("S08-10", "拓展分层", "05_课堂备课包/<周包>/10_拓展分层/"),
    ("S09", "实施 · 评价 · 改进", "06_课程实施/ + 07_优化与运维/ + 08_申报与成果/"),
]


# ========================= 二、基础工具 =========================

def mkdir(path: Path) -> None:
    """建目录（幂等）。"""
    created = not path.exists()
    path.mkdir(parents=True, exist_ok=True)
    print(("新建目录: " if created else "已存在  : ") + str(path))


def write_md(path: Path, title: str, body: str, overwrite: bool) -> None:
    """写轻量占位 md。默认不覆盖已存在文件——呼应「回退不删原文件」纪律。"""
    if path.exists() and not overwrite:
        print(f"跳过文件: {path}（已存在，未覆盖）")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
    print(f"新建文件: {path}")


def top_name(base: str, suffix: str, annotate: bool) -> str:
    """顶层目录名：默认跟 K02 磁盘（不带括号后缀）；--annotate-steps 时带上。"""
    return f"{base}{suffix}" if annotate else base


def pkg_name(week: int) -> str:
    """周备课包目录名。S07 定稿后应重命名为 备课包_第N周_作品X_具体主题。"""
    return f"备课包_第{week}周_作品待定_主题待定"


# ========================= 三、各区块生成 =========================

def build_top_and_subs(course_root: Path, annotate: bool) -> dict:
    """建 00–08 + 99 顶层目录及其固定子目录，返回 {基础名: 实际路径}。"""
    resolved = {}
    for base, suffix, note in TOP_DIRS:
        d = course_root / top_name(base, suffix, annotate)
        mkdir(d)
        resolved[base] = d
        for rel in SUB_DIRS.get(base, []):
            mkdir(d / rel)
    return resolved


def build_placeholders(dirs: dict, course_name: str, direction: str,
                       weeks: int, overwrite: bool) -> None:
    """在各 S0x 目录内生成轻量占位 md（命名对齐 K02）。"""
    meta = f"> 课程：{course_name}　方向：{direction}\n"
    todo = "本文件为占位，正文待对应步骤经审批门确认后填充。"

    d01 = dirs["01_工作调研与课程标准"]
    write_md(d01 / "S01_职业分析与就业调研" / "就业调研报告.md",
             f"{course_name} · S01 就业与职业分析调研报告",
             meta + f"\n待 S01 填充：区域产业带 / 岗位群 / 招聘样本与薪资 / 证书与认证。\n\n{todo}", overwrite)
    write_md(d01 / "S01_职业分析与就业调研" / "岗位能力清单.md",
             f"{course_name} · S01 岗位能力清单（DACUM）",
             meta + f"\n待 S01 填充：岗位 → 职责 → 任务 → 能力条目。\n\n{todo}", overwrite)
    write_md(d01 / "S02_典型工作任务分析（含案例台账）" / "典型工作任务分析.md",
             f"{course_name} · S02 典型工作任务分析",
             meta + f"\n待 S02 填充：典型工作任务清单 / 工作过程六要素 / 与 S01 岗位的映射。\n\n{todo}", overwrite)
    write_md(d01 / "S02_典型工作任务分析（含案例台账）" / "案例台账" / "案例台账.md",
             f"{course_name} · S02 案例台账",
             meta + "\n待 S02 填充：案例名 / 来源 / 对应典型任务 / 可用子步 / 素材路径。\n"
                    "纪律：素材实体统一放 `02_教学资源/案例库/cases/`，本台账只放指针，不重复存。\n", overwrite)
    write_md(d01 / "S03_能力图谱与技能点（PGSD）" / "能力图谱_PGSD.md",
             f"{course_name} · S03 能力图谱（PGSD 四维）",
             meta + f"\n待 S03 填充：P 专业 / G 通用 / S 社会 / D 发展 四维能力点。\n\n{todo}", overwrite)
    write_md(d01 / "S03_能力图谱与技能点（PGSD）" / "技能点分级标准.md",
             f"{course_name} · S03 技能点分级标准",
             meta + f"\n待 S03 填充：每个能力点的 初级=合格 / 中级=良好 / 高级=优秀 描述。\n\n{todo}", overwrite)
    write_md(d01 / "S04_课程标准" / "课程标准.md",
             f"{course_name} · S04 课程标准",
             meta + "\n待 S04 填充：课程定位 / 就业面向 / PGSD 能力目标 / 模块骨架 M1…Mn / 评价框架 / 岗课赛证口径。\n"
                    "纪律：只到模块层，不绑项目·作品·周次；**不得**命名为「课程标准（整体设计）」。\n", overwrite)

    d02 = dirs["02_教学资源"]
    write_md(d02 / "README.md", f"{course_name} · 02 教学资源共享池",
             meta + "\n- `案例库/cases/`：全课程唯一案例素材实体存放处（S02 台账指向此处）。\n"
                    "- `建设工具包/`：脚本 / 模板 / 工具压缩包。\n"
                    "- `教材与学材/`：教材初稿、学材母本（S08-4 引用）。\n", overwrite)

    d03 = dirs["03_学情与整体设计"]
    write_md(d03 / "S05_学生画像与学情" / "学生画像与学情分析.md",
             f"{course_name} · S05 学生画像与学情分析",
             meta + f"\n待 S05 填充：起点能力 / 认知特征 / 学习风格 / 差异化分层（ZPD）。\n\n{todo}", overwrite)
    write_md(d03 / "S06_课程整体设计" / "课程整体设计.md",
             f"{course_name} · S06 课程整体设计",
             meta + f"\n待 S06 填充：项目载体 / 作品链 / 学时分配 / 运营机制。\n\n{todo}", overwrite)
    write_md(d03 / "S06_课程整体设计" / f"{weeks}周教学进程表.md",
             f"{course_name} · S06 {weeks} 周教学进程表",
             meta + f"\n待 S06 填充：第 1–{weeks} 周 × 作品 / 任务 / 学时 / 交付物。\n"
                    "纪律：周进程属整体设计，**不进课程标准**。\n", overwrite)
    write_md(d03 / "S06_课程整体设计" / "模块×作品调用矩阵.md",
             f"{course_name} · S06 模块 × 作品调用矩阵",
             meta + "\n待 S06 填充：课标模块 M1…Mn（行） × 作品 1…n（列），标记调用强度，用于目标纵向一致性回溯。\n", overwrite)

    d04 = dirs["04_单元教学设计"]
    write_md(d04 / f"单元设计总览_{course_name}_{weeks}周.md",
             f"{course_name} · S07 单元设计总览（{weeks} 周）",
             meta + f"\n待 S07 填充：第 1–{weeks} 周单元一览（周次 / 作品 / 主题 / 能力点 / 评价方式）。\n"
                    "逐周文件命名：`单元设计_第N周_作品X_主题.md`，须与 05 备课包周包目录逐字对应。\n", overwrite)

    d05 = dirs["05_课堂备课包"]
    write_md(d05 / "说明与规格" / "备课包内容结构与归档规范.md",
             f"{course_name} · S08 备课包内容结构与归档规范",
             meta + "\n周包目录：`备课包_第N周_作品X_主题/`，内含 11 个子目录：\n"
                    "`00_本包说明`（包头）+ `01_工作页`…`10_拓展分层`（对应 S08-1…S08-10）。\n"
                    "顺序纪律（UbD 反向设计）：证据（01–03）先于教学（04–08），最后保障与差异化（09–10）。\n", overwrite)
    write_md(d05 / "说明与规格" / "资源规格映射表.md",
             f"{course_name} · S08 资源规格映射表",
             meta + "\n待填充：各子步产出的文件格式 / 命名 / 时长 / 分辨率 / 交付标准。\n", overwrite)
    write_md(d05 / "考核评价" / "README.md",
             f"{course_name} · 课程级考核评价汇总",
             meta + "\n课程级题库与量规汇总（周级实操在各周包 02_考题 / 03_量规）。待 S09 回流汇总。\n", overwrite)
    write_md(d05 / "数字化资源" / "脚本清单" / "微课与动画脚本清单.md",
             f"{course_name} · 微课与动画脚本清单",
             meta + "\n待 S08-7 / S08-8 填充：脚本编号 / 对应周次 / 时长 / 状态。\n", overwrite)

    d06 = dirs["06_课程实施"]
    write_md(d06 / "实施阶段规划与模板.md", f"{course_name} · S09 实施阶段规划与模板",
             meta + "\n待 S09 填充：开课准备 / 课堂实录留痕 / 实训组织 / 学生作品归档规则。\n", overwrite)

    d07 = dirs["07_优化与运维"]
    write_md(d07 / "运维改进规划与模板.md", f"{course_name} · S09 运维改进规划与模板",
             meta + "\n待 S09 填充：数据回流口径 / 反馈收集 / 版本迭代记录 / 建设总结（PDCA）。\n", overwrite)

    write_md(dirs["00_参考资料"] / "说明.md", f"{course_name} · 00 参考资料",
             meta + "\n存放：平台指南 / 行业标准 / 备课教程等跨步骤参考材料（与 02 教学资源同为共享性质）。\n", overwrite)
    write_md(dirs["08_申报与成果"] / "说明.md", f"{course_name} · 08 申报与成果",
             meta + "\n存放：精品课申报书 / 获奖材料 / 论文 / `历史版本/` 归档。\n", overwrite)
    write_md(dirs["99_工程与脚本"] / "说明.md", f"{course_name} · 99 工程与脚本",
             meta + "\n存放：一次性生成脚本、批处理工具（归档用，不参与教学交付）。\n", overwrite)


def build_packages(dirs: dict, course_name: str, sample_weeks: int, overwrite: bool) -> None:
    """预建示例周备课包骨架（每包 11 个子目录）。默认只建第 1 周作为模板。"""
    d05 = dirs["05_课堂备课包"]
    for week in range(1, sample_weeks + 1):
        pkg = d05 / pkg_name(week)
        mkdir(pkg)
        for sub in PKG_SUBDIRS:
            mkdir(pkg / sub)
        write_md(pkg / "00_本包说明" / "本包说明.md",
                 f"{course_name} · 备课包 第 {week} 周 · 本包说明",
                 "> 本包为 S07 定稿前的占位模板；确定周主题后，请把本目录重命名为\n"
                 f"> `备课包_第{week}周_作品X_具体主题`，与 `04_单元教学设计/单元设计_第{week}周_…` 逐字对应。\n\n"
                 "## 交付清单（S08 十子步，逐子步过审批门）\n\n"
                 "| 子步 | 目录 | 状态 |\n|---|---|---|\n"
                 "| S08-1 工作页 | 01_工作页/ | 待做 |\n"
                 "| S08-2 考题 | 02_考题/ | 待做 |\n"
                 "| S08-3 量规 | 03_量规/ | 待做 |\n"
                 "| S08-4 学材 | 04_学材/ | 待做 |\n"
                 "| S08-5 讲稿 | 05_讲稿/ | 待做 |\n"
                 "| S08-6 PPT | 06_PPT/ | 待做 |\n"
                 "| S08-7 动画 | 07_动画/ | 待做 |\n"
                 "| S08-8 微课 | 08_微课/ | 待做 |\n"
                 "| S08-9 设备耗材安全 | 09_设备耗材安全/ | 待做 |\n"
                 "| S08-10 拓展分层 | 10_拓展分层/ | 待做 |\n\n"
                 "顺序纪律（UbD）：01–03 评估证据 → 04–08 教学活动 → 09–10 保障与差异化。\n",
                 overwrite)


# ========================= 四、根文档 =========================

def tree_text(annotate: bool) -> str:
    """根文档用的目录树文本。"""
    t = lambda b, s: top_name(b, s, annotate)  # noqa: E731
    return f"""```text
├─ {t('00_参考资料', '')}/                       共享：平台指南 · 行业标准 · 备课教程
├─ {t('01_工作调研与课程标准', '（S01–S04）')}/    ← S01–S04，止于课标
│   ├─ S01_职业分析与就业调研/
│   ├─ S02_典型工作任务分析（含案例台账）/ └─ 案例台账/
│   ├─ S03_能力图谱与技能点（PGSD）/
│   └─ S04_课程标准/
├─ {t('02_教学资源', '')}/                       共享池：案例库/cases · 建设工具包 · 教材与学材
├─ {t('03_学情与整体设计', '（S05·S06）')}/
│   ├─ S05_学生画像与学情/
│   └─ S06_课程整体设计/ └─ 作品级教学设计/
├─ {t('04_单元教学设计', '（S07）')}/             逐周单元设计 + 总览
├─ {t('05_课堂备课包', '（S08）')}/
│   ├─ 说明与规格/
│   ├─ 备课包_第N周_作品X_主题/   ← 00_本包说明 + 01…10 共 11 个子目录
│   ├─ 数字化资源/脚本清单/
│   └─ 考核评价/
├─ {t('06_课程实施', '（S09·实施）')}/            授课实录 · 实训指导 · 学生作品
├─ {t('07_优化与运维', '（S09·改进）')}/          反馈与改进 · 版本迭代 · 建设总结
├─ {t('08_申报与成果', '')}/历史版本/
├─ {t('99_工程与脚本', '')}/一次性脚本/
└─ README.md · 目录结构清单.md · 课程文件夹结构设计（全周期）.md · 课程建设进度状态表.md
```"""


def build_root_docs(course_root: Path, course_name: str, direction: str,
                    weeks: int, annotate: bool, overwrite: bool) -> None:
    tree = tree_text(annotate)

    write_md(course_root / "README.md", f"{course_name} 课程建设工作区",
             f"> 方向：{direction}　周数：{weeks}　方法论：高职课程建设九步法 S01–S09（S08 展开 10 子步 = 18 步）\n\n"
             f"## 目录结构\n\n{tree}\n\n"
             "## 建设纪律\n\n"
             "1. 顺序铁律：S02 典型任务 在 S04 课标之前；S05 学生画像 在 S06 整体设计之前；周进程属 S06，不进课标。\n"
             "2. 三层文件：课程标准(S04) → 整体设计(S06) → 单元设计(S07)，抽象到具体逐层派生。\n"
             "3. 目标纵向一致：典型任务 → 课标能力点 → 整体设计项目 → 单元周任务 → 备课包考题，下层可回溯上层。\n"
             "4. **运行协议**：每步（含 S08 十子步）执行前报计划、执行后报成果，**必须等用户确认才进入下一步**；\n"
             "   可随时回退到任意已完成步骤，回退后下游标记 `⚠ 需重做`，原文件保留不删。\n"
             "   进度以 `课程建设进度状态表.md` 为唯一事实源。\n", overwrite)

    write_md(course_root / "目录结构清单.md", f"{course_name} · 目录结构清单（当前生效版）",
             f"> 对齐：高职课程建设九步法（S01–S09）+ 四阶段理论\n"
             f"> 命名纪律：课程标准 ≠ 课程整体设计（两层分离，不混用）；一级目录 `两位数字_中文`；不使用「特定证书体系」表述。\n\n"
             f"## 顶层目录（00–08 + 99，连续编号）\n\n{tree}\n\n"
             "## 九步法 → 目录映射\n\n"
             "| 步 | 理论阶段 | 落点 |\n|---|---|---|\n"
             "| S01 职业分析 | 职业分析 | 01/S01 |\n"
             "| S02 典型任务（含案例台账） | 职业分析 | 01/S02（案例素材实体在 02/案例库/cases） |\n"
             "| S03 能力图谱（PGSD） | 职业分析 | 01/S03 |\n"
             "| S04 课程标准 | 课程设计 | 01/S04 |\n"
             "| S05 学生画像 | 教学开发 | 03/S05 |\n"
             "| S06 课程整体设计 | 教学开发 | 03/S06 |\n"
             "| S07 单元设计 | 教学开发 | 04 |\n"
             "| S08 备课包（10 子步） | 教学开发 | 05（含数字化资源 + 考核评价） |\n"
             "| S09 实施·评价·改进 | 实施改进 | 06 实施 + 07 运维 + 08 申报（评价证据在 05） |\n", overwrite)

    write_md(course_root / "课程文件夹结构设计（全周期）.md",
             f"{course_name} 课程知识库 · 文件夹结构设计（全周期）",
             "## 一、理论脊柱（四阶段 / 九步）\n\n```text\n"
             "阶段一 职业分析与任务提炼：S01 职业分析 · S02 典型任务(含案例台账) · S03 能力图谱\n"
             "阶段二 课程设计          ：S04 课程标准\n"
             "阶段三 教学开发          ：S05 学生画像 · S06 整体设计 · S07 单元设计 · S08 备课包(10子步)\n"
             "阶段四 实施改进          ：S09 实施 → 评价 → 回流修订\n```\n\n"
             f"## 二、最终结构（10 个一级 + 根文档）\n\n{tree}\n\n"
             "## 三、设计要点\n\n"
             "1. **01 止于 S04**：职业分析→典型任务→能力图谱→课程标准是一条产出「能力母本」的链，到课标为止。\n"
             "2. **02 提为根级共享池**：案例 / 工具包 / 教材是跨步骤共享资源，与 00_参考资料 同性质。\n"
             "3. **03 = 学情 + 整体设计**：学生画像是整体设计的输入，同属教学开发准备层。\n"
             "4. **05 备课包并入数字化资源 + 考核评价**：微课 / 动画 / 题库 / 量规本就是 S08 子步产出。\n"
             "5. **备课包按 UbD 反向设计排序**：证据（工作页→考题→量规）先于教学（学材→讲稿→PPT→动画→微课），\n"
             "   最后保障与差异化（设备耗材安全→拓展分层）。\n\n"
             "## 四、命名纪律\n\n"
             "- 一级目录：`两位数字_中文`（00…08、99）。\n"
             "- 不写「课程标准（整体设计）」；课标与整体设计是两层不同交付物。\n"
             "- 去日期化：不带 `2026-07-xx` 之类来源后缀。\n"
             "- 重复文件只留一份；素材实体唯一存放于 `02_教学资源/案例库/cases/`。\n", overwrite)


def build_progress_table(course_root: Path, course_name: str,
                         sample_weeks: int, overwrite: bool) -> None:
    """生成进度状态表（技能运行协议的唯一进度事实源）。"""
    pkg = pkg_name(1)
    rows = []
    for code, name, loc in STEPS:
        loc = loc.replace("<周包>", pkg)
        rows.append(f"| {code} {name} | 待做 | {loc} | — |")
    body = (
        "> 状态取值：`待做` / `进行中` / `已确认` / `⚠ 需重做` / `已跳过（原因：…）`\n"
        "> 本表是课程建设进度的**唯一事实源**。每次步骤状态变更必须同步更新本文件并贴给用户。\n"
        f"> 已预建示例周备课包：第 1–{sample_weeks} 周（S08 行以第 1 周为例；多周时按周复制 S08-1…S08-10 十行）。\n\n"
        "| 步骤 | 状态 | 产出文件 / 落点 | 备注 |\n|---|---|---|---|\n"
        + "\n".join(rows) + "\n\n"
        "## 回退级联影响表\n\n"
        "| 被修改步骤 | 需标记 `⚠ 需重做` 的下游 |\n|---|---|\n"
        "| S01 | S02 S03 S04 S05 S06 S07 S08-1…10 S09 |\n"
        "| S02 | S03 S04 S06 S07 S08-1…10 |\n"
        "| S03 | S04 S06 S07 S08-1 S08-2 S08-3 |\n"
        "| S04 | S06 S07 S08-1…10 |\n"
        "| S05 | S06 S07 S08-10 |\n"
        "| S06 | S07 S08-1…10 |\n"
        "| S07 | S08-1…10 |\n"
        "| S08-1 | S08-2 S08-3 S08-4 S08-5 |\n"
        "| S08-2 / S08-3 | S08-5 S08-6 |\n"
        "| S08-4…S08-8 | （同级互检，无强制下游） |\n"
        "| S08-9 / S08-10 | （无下游） |\n"
        "| S09 | 回流修订 → 由用户指定回到哪一步 |\n"
    )
    write_md(course_root / "课程建设进度状态表.md",
             f"{course_name} · 课程建设进度状态表（18 步）", body, overwrite)


# ========================= 五、主流程 =========================

def create(root: str, course_name: str, direction: str, code: str, weeks: int,
           sample_weeks: int, annotate: bool, overwrite: bool) -> Path:
    folder = f"{code}_{course_name}" if code else course_name
    course_root = Path(root).expanduser() / folder
    mkdir(course_root)

    dirs = build_top_and_subs(course_root, annotate)
    build_placeholders(dirs, course_name, direction, weeks, overwrite)
    build_packages(dirs, course_name, sample_weeks, overwrite)
    build_root_docs(course_root, course_name, direction, weeks, annotate, overwrite)
    build_progress_table(course_root, course_name, sample_weeks, overwrite)

    print(f"\n骨架就绪：{course_root}")
    print(f"顶层目录 {len(TOP_DIRS)} 个（00–08 + 99）；示例周备课包 {sample_weeks} 个（每包 {len(PKG_SUBDIRS)} 个子目录）。")
    print("下一步：进入 S01 审批门 ①「报计划」，等用户确认后再开始写正文。")
    return course_root


def main() -> None:
    p = argparse.ArgumentParser(
        description="创建高职课程建设工作区骨架（00–08 + 99，对齐 K02 权威结构）")
    p.add_argument("--root", required=True, help="课程文件夹存放的父目录，如 ~/WorkBuddy")
    p.add_argument("--course-name", required=True, help="课程名称，如 某专业核心课")
    p.add_argument("--direction", required=True, help="课程方向关键词，如 短视频·微短剧")
    p.add_argument("--code", default="", help="课程编号前缀，可选，如 K03（生成 K03_课程名）")
    p.add_argument("--weeks", type=int, default=14, help="课程总周数，默认 14（影响进程表与单元总览命名）")
    p.add_argument("--sample-weeks", type=int, default=1,
                   help="预建示例周备课包数量，默认 1（其余周次待 S07 定稿后按需建）")
    p.add_argument("--annotate-steps", action="store_true",
                   help="顶层目录名带步骤标注后缀（如 01_工作调研与课程标准（S01–S04））；默认不带，跟 K02 磁盘一致")
    p.add_argument("--overwrite", action="store_true",
                   help="覆盖已存在的占位文件（默认不覆盖，保护已填写内容）")
    a = p.parse_args()
    create(a.root, a.course_name, a.direction, a.code, a.weeks,
           a.sample_weeks, a.annotate_steps, a.overwrite)


if __name__ == "__main__":
    main()
