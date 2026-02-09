# -*- coding: utf-8 -*-
"""
コードブロック直前の見出しを #### から ### に変更
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def change_code_headings(file_path: Path):
    """コードブロック直前の####を###に変更"""
    content = file_path.read_text(encoding="utf-8")
    original = content
    
    # #### ファイル名\n```c パターンを ### ファイル名\n```c に変更
    content = re.sub(
        r'^####\s+([^\n]+)\n+(```c)',
        r'### \1\n\n\2',
        content,
        flags=re.M
    )
    
    if content != original:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    print("コードブロック見出しを #### → ### に変更中...\n")
    
    fixed_count = 0
    
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        if change_code_headings(file_path):
            print(f"✓ {file_path.name}")
            fixed_count += 1
    
    print(f"\n完了: {fixed_count}ファイルを修正しました")

if __name__ == "__main__":
    main()
