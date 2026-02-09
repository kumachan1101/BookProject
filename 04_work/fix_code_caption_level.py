# -*- coding: utf-8 -*-
"""
SKILL.md 3.2修正 v2: ### をコード直前では #### に変換
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def fix_code_caption_headings(file_path: Path):
    """コードブロック直前の### を#### に変換"""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    modified = False
    new_lines = []
    
    for i in range(len(lines)):
        line = lines[i]
        
        # 次の行がコードブロックかチェック
        is_before_code = False
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            # 空行をスキップして次の実質的な行を探す
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                next_real_line = lines[j].strip()
                if next_real_line.startswith('```c'):
                    # 実行結果セクションでないかチェック
                    context_start = max(0, i - 10)
                    context = '\n'.join(lines[context_start:i+1])
                    is_result = any(keyword in context for keyword in ['実行結果', '出力例', '実行例', '実行時の出力'])
                    if not is_result:
                        is_before_code = True
        
        # ### で始まり、コード直前の場合は #### に変換
        if is_before_code and line.strip().startswith('###') and not line.strip().startswith('####'):
            # ### を #### に変換
            new_line = line.replace('###', '####', 1)
            new_lines.append(new_line)
            modified = True
        else:
            new_lines.append(line)
    
    if modified:
        new_content = '\n'.join(new_lines)
        file_path.write_text(new_content, encoding="utf-8")
    
    return modified

def main():
    print("コード直前見出しレベル修正開始...\n")
    
    fixed_count = 0
    
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        if fix_code_caption_headings(file_path):
            print(f"✓ {file_path.name}")
            fixed_count += 1
    
    print(f"\n完了: {fixed_count}ファイルを修正しました")

if __name__ == "__main__":
    main()
