#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S07 单元设计批量注入脚本（固化自职教课程建设实践）
为 <src>/ 下除「第1周」样板外的所有「单元设计_第*.md」，注入「学校模板对齐速填区（九节）」，
保留原文（BOtPPPS 详细设计）。可靠字段自动提取，语义字段（学情/K-S-A/作业/评价/R编码）留占位待人工复核。

用法：
  cd <课程根目录>
  python3 scripts/inject_unit_align.py --dry      # 仅打印每周围提取摘要，不写文件
  python3 scripts/inject_unit_align.py            # 实际写入（在首个「## 板块1：基本信息」前插入对齐区）
  python3 scripts/inject_unit_align.py --src 04_单元教学设计   # 指定单元目录（默认相对 cwd 的 04_单元教学设计）

注：课程名/教师/学时等为 K02 示例值；复用其他课程时按 `S07单元设计骨架约定.md` 调整 gen_align 内常量。
"""
import re, os, sys, glob, argparse

parser = argparse.ArgumentParser(description="S07 单元批量注入学校模板对齐速填区")
parser.add_argument("--src", default="04_单元教学设计", help="单元设计目录（相对 cwd 或绝对）")
args = parser.parse_args()
BASE = args.src

def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()

def write(p, s):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)

def grab(md, pat, flags=re.S):
    m = re.search(pat, md, flags)
    return m.group(1).strip() if m else ''

def extract(md):
    out = {}
    b1 = grab(md, r'## 板块1：基本信息\s*\n(.*?)(?=\n## 板块2)', re.S)
    out['obj']   = grab(b1, r'\|\s*授课对象\s*\|\s*(.*?)\s*\|')
    out['hours'] = grab(b1, r'\|\s*课时\s*\|\s*(.*?)\s*\|')
    out['sizu']  = grab(b1, r'\|\s*课程思政融入点\s*\|\s*(.*?)\s*\|')
    out['gksz']  = grab(b1, r'\|\s*岗课赛证对接点\s*\|\s*(.*?)\s*\|')
    b2 = grab(md, r'## 板块2：学习任务\s*\n(.*?)(?=\n## 板块3)', re.S)
    out['result'] = grab(b2, r'\|\s*本单元预期成果\s*\|\s*(.*?)\s*\|')
    out['taskpos'] = grab(b2, r'\|\s*本单元在课程 / 项目中的位置\s*\|\s*(.*?)\s*\|')
    b3 = grab(md, r'## 板块3：教学目标与重难点\s*', re.S) or grab(md, r'## 板块3：教学目标与重难点\s*\n(.*?)(?=\n## 板块4)', re.S)
    def list_items(sec):
        m = re.search(r'\*\*' + sec + r'[（(][^）)]*[）)]\s*\n(.*?)(?=\n###|\Z)', b3, re.S)
        if not m: return []
        return [l.strip().lstrip('0123456789. ').strip() for l in re.findall(r'^\d+\.\s*(.*)$', m.group(1), re.M)]
    out['kobj'] = list_items('知识目标')
    out['sobj'] = list_items('能力目标')
    out['aobj'] = list_items('素养目标')
    b4 = grab(md, r'## 板块4：教学过程设计\s*\n(.*?)(?=\n## 板块5)', re.S)
    out['dur'] = grab(b4, r'课时合计校验\*\*：.*?=\s*\*\*?(\d+\s*min)')
    b6 = grab(md, r'## 板块6：教学资源清单\s*\n(.*?)(?=\n## 板块7)', re.S)
    rows = re.findall(r'^\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$', b6, re.M)
    res = []
    for r in rows:
        cat0, name = r[0].strip(), r[1].strip()
        if cat0 in ('资源类型','资源名称','') or name in ('资源名称','',):
            continue
        res.append((name, cat0))
    out['res'] = res[:10]
    return out

def o_code(week):
    if week <= 2:   return "**O1** 职业素养与规范认知（主） ／ **O2** 平台与岗位认知"
    if week <= 11:  return "**O2** 通用能力与内容策划（主） ／ **O3** 拍摄剪辑制作"
    return "**O4** 运营传播与 AI 融合（主） ／ **O2/O3** 综合"

def gen_align(week, title, ex):
    L = []
    L.append("## 学校单元设计模板对齐速填区（九节）\n")
    L.append("> 本节按学校 L2-3 单元设计模板九节结构速填，详细设计见下方各板块（BOtPPPS 主线）。五步法对照见节6。编码规则见 `S07单元设计骨架约定.md`。\n")
    L.append("### 节1 授课信息\n")
    L.append("| 项目 | 内容 |")
    L.append("|---|---|")
    L.append(f"| 授课教师 | 【待填·教师/部门/职称】 |")
    L.append(f"| 授课对象 | {ex['obj'] or '【待填】'} ／ 班级【待填】 ／ 人数【待填】 |")
    L.append(f"| 课程 | <课程名> ／ 理实一体 ／ 总学时 <N> |")
    L.append(f"| 单元 | 第{week}周·{title} ／ 4课时(180min) |")
    L.append(f"| 授课日期·地点 | 【待填】 ／ 智慧教室·实训机房 |\n")
    L.append("### 节2 任务分析\n")
    L.append("| 项目 | 内容 |")
    L.append("|---|---|")
    L.append(f"| 任务名称 | {title}")
    L.append(f"| 发生情境 | S02 典型任务（详见整体设计作品级教学设计） |")
    L.append(f"| 实施过程 | {ex['result'] or '【待填】'} |")
    L.append(f"| 所需资源 | 见节5 资源清单 |")
    L.append(f"| 结果要求 | {ex['result'] or '【待填】'} |")
    L.append(f"| 能力要素 | PGSD（详见板块3目标与课标四维） |")
    L.append(f"| 教材利用 | 校本教材 + 企业资源（品牌手册等） |\n")
    L.append("### 节3 学情分析\n")
    L.append("| 分析因素 | 分析因素 | 有利于教学 | 不利于教学 |")
    L.append("|---|---|---|---|")
    L.append("| 准备状态 | 心理准备 | 刷短视频经验丰富、兴趣高 | 视为娱乐，未建立学习动机 |")
    L.append("| 准备状态 | 能力准备 | 会用剪映基础、有拍摄经验 | 缺结构化分析方法 |")
    L.append("| 认知特点 | 学习风格 | 视觉/案例驱动 | 纯讲授易走神 |")
    L.append("| 认知特点 | 学习方法 | 小组协作意愿强 | 主动探究弱 |")
    L.append("| 应对措施 | 应对措施 | 用真实案例示证降低门槛 | 提供支架表、激活旧知 |\n")
    L.append("### 节4 学习目标\n")
    L.append("| 项目 | 内容 |")
    L.append("|---|---|")
    L.append(f"| 学习结果 O | {o_code(week)} |")
    ktxt = "；".join(ex['kobj']) or "【待按 PGSD↔KSA 重编码】"
    stxt = "；".join(ex['sobj']) or "【待按 PGSD↔KSA 重编码】"
    atxt = "；".join(ex['aobj']) or "【待按 PGSD↔KSA 重编码】"
    L.append(f"| 支撑要素 K | K1 {ktxt} |")
    L.append(f"| 支撑要素 S | S1 {stxt} |")
    L.append(f"| 支撑要素 A | A1 {atxt} |")
    L.append(f"| 重点 | 【待填·由板块3重点提取】 ／ 措施：【待填】 |")
    L.append(f"| 难点 | 【待填·由板块3难点提取】 ／ 措施：【待填】 |\n")
    L.append("### 节5 教学资源（R编码）\n")
    L.append("> 资源明细见本文件「板块6：教学资源清单」原表；下表 R1–R10 为占位，请按 `S07单元设计骨架约定.md` 映射类别后填名称。\n")
    L.append("| 代码 | 名称 | 类别 |")
    L.append("|---|---|---|")
    for i in range(1, 11):
        L.append(f"| R{i} | 【待填·引板块6】 | 【待填】 |")
    L.append("")
    L.append("### 节6 教学过程（BOtPPPS 主线 + 五步法对照）\n")
    L.append(f"**BOtPPPS 六环节时长**：{ex['dur'] or '【待填·见板块4】'}\n")
    L.append("| 五步法 | 对应 BOtPPPS 环节 | 本单元落点 |")
    L.append("|---|---|---|")
    L.append("| 明确任务 | B导入+O目标+T前测 | 抛现象、明目标、激活旧知 |")
    L.append("| 制定计划 | P探究（计划子步） | 建立分析/操作框架 |")
    L.append("| 组织实施 | P探究（示证）+P应用 | 教师示证→学生应用 |")
    L.append("| 评估调控 | P后测+过程评价 | 检测题+量规互评 |")
    L.append("| 反思总结 | S总结+课后反思 | 出门条+PMIQ |\n")
    L.append("### 节7 课后作业\n")
    L.append("| 题号 | 题干 | 目的 | 配分 |")
    L.append("|---|---|---|---|")
    L.append("| 1 | 【待填·按板块7题库改造为配分作业】 | 巩固 | 【待填】 |")
    L.append("| 2 | 【待填】 | 应用 | 【待填】 |")
    L.append("| 合计 | | | 【待填】 |\n")
    L.append("### 节8 学习评价（结构化）\n")
    L.append("| 评价项目 | 配分 | 评分细则 |")
    L.append("|---|---|---|")
    L.append("| 课前任务 /（XX分） | 【待填】 | 引板块7.6量规课前维度 |")
    L.append("| 课中表现 /（XX分） | 【待填】 | 协作/参与/探究 |")
    L.append("| 课后作业 /（XX分） | 【待填】 | 作业质量 |\n")
    L.append("### 节9 课后反思\n")
    L.append("| 项目 | 内容 |")
    L.append("|---|---|")
    L.append("| 教学效果 | 【课后填】 |")
    L.append("| 特色创新 | 【课后填】 |")
    L.append("| 存在问题 | 【课后填】 |")
    L.append("| 改进措施 | 【课后填】 |\n")
    return "\n".join(L)

def main():
    dry = '--dry' in sys.argv
    files = sorted(glob.glob(os.path.join(BASE, "单元设计_第*.md")))
    files = [f for f in files if "第1周" not in os.path.basename(f)]  # 第1周为已填样板，跳过
    print(f"[inject_unit_align] 待处理文件数: {len(files)}  dry={dry}")
    for p in files:
        fn = os.path.basename(p)
        wm = re.search(r'第(\d+)周', fn)
        week = int(wm.group(1)) if wm else 0
        md = read(p)
        if '学校单元设计模板对齐速填区' in md:
            print(f"  跳过(已注入): {fn}")
            continue
        ex = extract(md)
        title = fn.split('_', 2)[-1].replace('.md','') if fn.startswith('单元设计_') else fn
        align = gen_align(week, title, ex)
        anchor = "\n## 板块1：基本信息"
        idx = md.find(anchor)
        if idx == -1:
            print(f"  !! 未找到锚点(板块1)，跳过: {fn}")
            continue
        new_md = md[:idx] + "\n" + align + "\n---\n" + md[idx:]
        if dry:
            print(f"  [DRY] {fn} 周{week} 对象={ex['obj'][:30]!r} 时长={ex['dur']!r} 资源数={len(ex['res'])} K目标={len(ex['kobj'])} S目标={len(ex['sobj'])}")
        else:
            write(p, new_md)
            print(f"  [OK] 已注入: {fn}")
    print("[inject_unit_align] 完成。")

if __name__ == '__main__':
    main()
