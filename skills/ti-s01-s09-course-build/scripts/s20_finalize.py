# -*- coding: utf-8 -*-
"""S20 一键收尾：校验 + 常见修复 + 报告（骨架版）
用法: python s20_finalize.py --base <课程根> --course <课程名>
"""
import sys, os, argparse, subprocess, json

def main():
    parser = argparse.ArgumentParser(description='S20 一键收尾')
    parser.add_argument('--base', default=os.getcwd(), help='课程根目录')
    parser.add_argument('--course', default='', help='课程名')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    checker = os.path.join(script_dir, 'check_s20_integrity.py')
    report = {'passed': [], 'fixed': [], 'remaining': []}

    print('=' * 50)
    print(f'S20 一键收尾：{args.course or "课程"} @ {args.base}')
    print('=' * 50)

    # 1. 运行校验
    print('\n[1/4] 运行完整性校验...')
    cmd = [sys.executable, checker, '--base', args.base]
    if args.course:
        cmd += ['--course', args.course]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    out = r.stdout + r.stderr
    print(out[-2000:] if len(out) > 2000 else out)

    # 2. 自动修复常见问题（骨架：列出可修复项）
    print('\n[2/4] 常见问题自动修复（骨架）...')
    fixes = {
        'S08授课计划缺学期锚点': '自动补"教学时数按学期分配"段落',
        '教案缺对齐区': '运行 inject_unit_align.py',
        'office骨架缺失': '运行 gen_office_skeletons.py',
        'S03扩展表缺列': '运行 add_map_cols.py',
    }
    for k, v in fixes.items():
        print(f'  - 可修复: {k} → {v}')

    # 3. 输出报告
    print('\n[3/4] 收尾报告（人工确认）')
    print('  修复建议见上；人工执行后重跑校验。')

    # 4. 生成报告文件
    report_path = os.path.join(args.base, '99_工程与脚本', 's20_finalize_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f'\n[4/4] 报告已存: {report_path}')
    print('完成。遗留问题请在报告中人工确认。')

if __name__ == '__main__':
    main()
