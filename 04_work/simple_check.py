# -*- coding: utf-8 -*-
"""
簡易SKILL準拠チェック - サマリーのみ
"""
import re
from pathlib import Path
import sys

# Windows環境でのUnicodeエラー回避
sys.stdout.reconfigure(encoding='utf-8')

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def check_file_compliance(file_path: Path):
    """ファイルのSKILL準拠を包括的にチェック"""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    issues = []
    
    # 1. コードブロック直前に#### があるかチェック
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```c'):
            context_start = max(0, i - 10)
            context = '\n'.join(lines[context_start:i])
            if any(keyword in context for keyword in ['実行結果', '出力例', '実行例', '実行時の出力']):
                continue
            
            prev_line_idx = i - 2
            if prev_line_idx >= 0:
                prev_line = lines[prev_line_idx].strip()
                while prev_line_idx >= 0 and not prev_line:
                    prev_line_idx -= 1
                    prev_line = lines[prev_line_idx].strip() if prev_line_idx >= 0 else ""
                
                if prev_line and not prev_line.startswith('####'):
                    issues.append({'type': 'code_format', 'line': i})
    
    # 2. ★マーカーチェック
    for i, line in enumerate(lines, 1):
        if '★' in line:
            issues.append({'type': 'star_marker', 'line': i})
    
    return issues

def main():
    print("SKILL準拠チェック実行中...\n")
    
    all_issues = {}
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        issues = check_file_compliance(file_path)
        if issues:
            all_issues[file_path.name] = issues
    
    if all_issues:
        print(f"問題検出: {len(all_issues)}ファイル\n")
        for filename, issues in all_issues.items():
            code_issues = [i for i in issues if i['type'] == 'code_format']
            star_issues = [i for i in issues if i['type'] == 'star_marker']
            print(f"{filename}: コード{len(code_issues)}件, 星{len(star_issues)}件")
    else:
        print("OK: 全ファイルがSKILL準拠です!")

if __name__ == "__main__":
    main()
