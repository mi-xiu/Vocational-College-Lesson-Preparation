#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package_team.py —— 职教课程开发专家团「打包功能」

把专家团队包（agents / skills / templates / avatars / knowledge / 文档）
打成带语义版本号的可分享压缩包，并附等价的 .wbp 离线安装副本，同时打印清单。

设计目标
--------
1. 单一命令产出可分发文件，免去手工 zip 漏文件 / 命名不一致。
2. 自动从 .codebuddy-plugin/plugin.json 读取 name + version，文件名含版本标识。
3. 团队包内嵌本脚本 → 团队包可「自我重新打包」，版本迭代后一键再分发。
4. 排除缓存 / 系统 / 备份类文件，控制体积（资料库上传上限 50 MiB）。

用法
----
    # 输出到默认「专家团分享包/」目录（位于团队包同级）
    python3 scripts/package_team.py <expert-dir>

    # 指定输出目录、不产 .wbp
    python3 scripts/package_team.py <expert-dir> --out-dir ~/Desktop --no-wbp

依赖：Python 3.8+，仅标准库（zipfile / shutil / json / os / argparse）。
"""
import argparse
import datetime
import json
import os
import shutil
import sys
import zipfile

# 需整体排除的目录名
EXCLUDE_DIRS = {".git", "__pycache__", "_backup", "node_modules", ".venv", "venv", "dist", "build"}
# 需排除的文件名
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", ".gitignore", ".gitkeep"}
# 需排除的文件后缀
EXCLUDE_SUFFIXES = (".pyc", ".pyo", ".tmp", ".swp", ".bak", "~")
# 允许保留的隐藏目录（其余隐藏目录一律排除）
KEEP_HIDDEN_DIRS = {".codebuddy-plugin"}


def load_meta(expert_dir):
    """读取团队包版本与名称。优先 .codebuddy-plugin/plugin.json，回退 plugin.json。"""
    for cand in (".codebuddy-plugin/plugin.json", "plugin.json"):
        pj = os.path.join(expert_dir, cand)
        if os.path.isfile(pj):
            with open(pj, encoding="utf-8") as f:
                meta = json.load(f)
            name = meta.get("name") or os.path.basename(expert_dir.rstrip("/"))
            version = meta.get("version", "0.0.0")
            return name, version, pj
    raise FileNotFoundError("未找到 plugin.json（团队包结构异常）")


def _is_excluded(rel_path):
    parts = rel_path.split(os.sep)
    base = parts[-1]
    if base in EXCLUDE_FILES or base in EXCLUDE_DIRS:
        return True
    if any(base.endswith(s) for s in EXCLUDE_SUFFIXES):
        return True
    # 排除任意 .bak / .bak1 / .bak2 等备份后缀（.bak 已在 EXCLUDE_SUFFIXES，此处兜底变体）
    if ".bak" in base and base.rsplit(".", 1)[-1].startswith("bak"):
        return True
    for part in parts[:-1]:  # 非末级的隐藏目录（保留名单除外）
        if part.startswith(".") and part not in KEEP_HIDDEN_DIRS:
            return True
    if parts[0].startswith(".") and parts[0] not in KEEP_HIDDEN_DIRS:
        return True
    return False


def collect_files(expert_dir):
    collected = []
    for cur, dirs, fns in os.walk(expert_dir):
        # 原地剪枝：排除指定目录与隐藏目录（保留名单除外）
        dirs[:] = [
            d for d in dirs
            if d not in EXCLUDE_DIRS
            and not (d.startswith(".") and d not in KEEP_HIDDEN_DIRS)
        ]
        for fn in fns:
            fp = os.path.join(cur, fn)
            rel = os.path.relpath(fp, expert_dir)
            if _is_excluded(rel):
                continue
            collected.append((fp, rel))
    collected.sort(key=lambda x: x[1])
    return collected


def build(expert_dir, out_dir, make_wbp):
    expert_dir = os.path.abspath(expert_dir)
    if not os.path.isdir(expert_dir):
        print(json.dumps({"error": f"团队包目录不存在: {expert_dir}"}))
        sys.exit(1)

    name, version, meta_path = load_meta(expert_dir)
    os.makedirs(out_dir, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d")
    base = f"{name}-v{version}"
    zip_path = os.path.join(out_dir, base + ".zip")

    files = collect_files(expert_dir)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for fp, rel in files:
            z.write(fp, rel)

    size = os.path.getsize(zip_path)
    print(f"KS_PACKAGE_OK name={name} version={version} meta={meta_path}")
    print(f"KS_PACKAGE_FILES count={len(files)} size_bytes={size} zip={zip_path}")

    if make_wbp:
        wbp_path = os.path.join(out_dir, base + ".wbp")
        shutil.copyfile(zip_path, wbp_path)
        print(f"KS_PACKAGE_WBP {wbp_path}")

    # 控制台可读摘要
    print(f"\n✅ 打包完成：{base}")
    print(f"   文件数：{len(files)}")
    print(f"   体积  ：{size/1024/1024:.2f} MiB")
    print(f"   zip   ：{zip_path}")
    if make_wbp:
        print(f"   wbp   ：{wbp_path}")
    return zip_path, base, version, len(files), size


def main():
    ap = argparse.ArgumentParser(description="职教课程开发专家团打包功能")
    ap.add_argument("expert_dir", help="团队包根目录（含 .codebuddy-plugin/plugin.json）")
    ap.add_argument("--out-dir", default=None, help="输出目录，默认团队包同级「专家团分享包/」")
    ap.add_argument("--no-wbp", action="store_true", help="不生成 .wbp 离线安装副本")
    args = ap.parse_args()

    out_dir = args.out_dir or os.path.join(os.path.dirname(os.path.abspath(args.expert_dir)), "专家团分享包")
    build(args.expert_dir, out_dir, not args.no_wbp)


if __name__ == "__main__":
    main()
