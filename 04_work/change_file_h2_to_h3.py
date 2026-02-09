# -*- coding: utf-8 -*-
"""
コードブロック直前のH2見出しをH3に変更
パターン: ## ファイル名.c/h → ### ファイル名.c/h
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def change_file_headings(file_path: Path):
    """ファイル名見出しをH2からH3に変更"""
    content = file_path.read_text(encoding="utf-8")
    original = content
    
    # ## ファイル名.c または ## ファイル名.h のパターンを ### に変更
    # ただし、説明文の後に #### ファイル名 があるパターンのみ
    
    # より安全なアプローチ: ## で始まり、.c または .h で終わる行を ### に変更
    content = re.sub(
        r'^##\s+([^\n]+\.(c|h))\s*$',
        r'### \1',
        content,
        flags=re.M
    )
    
    if content != original:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    print("ファイル名見出しを ## → ### に変更中...\n")
    
    fixed_count = 0
    total_changes = 0
    
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        # 変更前後の ## の数をカウント
        before = file_path.read_text(encoding="utf-8").count('\n## ')
        
        if change_file_headings(file_path):
            after = file_path.read_text(encoding="utf-8").count('\n## ')
            changes = before - after
            print(f"✓ {file_path.name} ({changes}箇所)")
            fixed_count += 1
            total_changes += changes
    
    print(f"\n完了: {fixed_count}ファイル、{total_changes}箇所を修正しました")

if __name__ == "__main__":
    main()
