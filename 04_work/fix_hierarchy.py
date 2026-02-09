# -*- coding: utf-8 -*-
"""
H2->H4 という見出し階層飛びを修正するスクリプト
H4の直前の見出しレベルが2だった場合、H4の直前に同名のH3を挿入する。
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def fix_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []
    
    last_heading_level = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 見出しレベル判定
        current_level = 0
        if stripped.startswith("#"):
            current_level = len(stripped.split()[0])
        
        # H4検知時の処理
        if current_level == 4:
            if last_heading_level == 2:
                # 階層飛び発生！ H3を挿入する
                h4_content = stripped.replace("####", "").strip()
                # コード例などの場合は少し調整してもいいが、基本はそのまま
                new_lines.append(f"### {h4_content}")
                last_heading_level = 3 # 補正
        
        # 行を追加
        new_lines.append(line)
        
        # レベル更新（空行などは無視、見出し行のみで更新）
        if current_level > 0 and current_level <= 4:
            last_heading_level = current_level

    # 保存
    new_content = "\n".join(new_lines)
    if content.endswith("\n") and not new_content.endswith("\n"):
        new_content += "\n"
        
    if new_content != content:
        print(f"Fixed hierarchy: {file_path.name}")
        file_path.write_text(new_content, encoding="utf-8")

def main():
    print("Fixing heading hierarchy (H2->H4)...")
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        fix_file(file_path)
    print("Done.")

if __name__ == "__main__":
    main()
