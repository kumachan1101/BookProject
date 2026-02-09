# -*- coding: utf-8 -*-
"""
強制的SKILL修正: コード直前の全ての見出しを#### に統一
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def force_fix_code_headings(file_path: Path):
    """コードブロック直前の見出しを強制的に#### に変換"""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    modified = False
    new_lines = []
    
    for i in range(len(lines)):
        line = lines[i]
        
        # 次の実質的な行がコードブロックかチェック
        is_before_code = False
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        
        if j < len(lines) and lines[j].strip().startswith('```c'):
            # 実行結果セクションでないかチェック
            context_start = max(0, i - 10)
            context = '\n'.join(lines[context_start:i+1])
            is_result = any(keyword in context for keyword in ['実行結果', '出力例', '実行例', '実行時の出力', '出力結果'])
            if not is_result:
                is_before_code = True
        
        # コード直前で、見出し(#で始まる)の場合、#### に統一
        if is_before_code and line.strip().startswith('#'):
            # 既存の#を全て削除して、####を追加
            heading_text = re.sub(r'^#+\s*', '', line.strip())
            new_line = '#### ' + heading_text
            new_lines.append(new_line)
            modified = True
        else:
            new_lines.append(line)
    
    if modified:
        new_content = '\n'.join(new_lines)
        file_path.write_text(new_content, encoding="utf-8")
    
    return modified

def main():
    print("強制的コード直前見出し修正開始...\n")
    
    fixed_count = 0
    
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        if force_fix_code_headings(file_path):
            print(f"✓ {file_path.name}")
            fixed_count += 1
    
    print(f"\n完了: {fixed_count}ファイルを修正しました")

if __name__ == "__main__":
    main()
