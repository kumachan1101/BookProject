# -*- coding: utf-8 -*-
"""
SKILL.md 3.2準拠チェック: コードブロック直前に#### ファイル名があるか
"""
import re
from pathlib import Path

def check_code_block_format(file_path: Path):
    """コードブロックの直前に#### ファイル名があるかチェック"""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    issues = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```c'):
            # 直前の行をチェック
            prev_line_idx = i - 2  # 0-indexed
            if prev_line_idx >= 0:
                prev_line = lines[prev_line_idx].strip()
                if not prev_line.startswith('####'):
                    # さらに前の行もチェック(空行がある場合)
                    if prev_line_idx > 0:
                        prev_prev_line = lines[prev_line_idx - 1].strip()
                        if not prev_prev_line.startswith('####'):
                            issues.append({
                                'line': i,
                                'prev_line': prev_line,
                                'issue': 'コードブロック直前に#### ファイル名がありません'
                            })
    
    return issues

# テスト
file_path = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\03_第1部 第1章 `static`キーワード - 情報隠蔽による依存の切断と実装の自由.md")
issues = check_code_block_format(file_path)

if issues:
    print(f"❌ {len(issues)}箇所の問題を検出:")
    for issue in issues:
        print(f"  L{issue['line']}: {issue['issue']}")
        print(f"    直前行: {issue['prev_line']}")
else:
    print("✅ 全てのコードブロックが正しくフォーマットされています")
