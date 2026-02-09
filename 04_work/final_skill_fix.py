# -*- coding: utf-8 -*-
"""
最終SKILL修正スクリプト: ## (続き) を #### に変換 + H2→H4 を H2→H3 に修正
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def final_fix(file_path: Path):
    """残りの全SKILL問題を修正"""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    modified = False
    new_lines = []
    
    # 1. ## (続き) や ## ファイル名 をコード直前では #### に変換
    for i in range(len(lines)):
        line = lines[i]
        
        # 次の行がコードブロックかチェック
        is_before_code = False
        if i + 1 < len(lines):
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
        
        # ## で始まり、コード直前の場合は #### に変換
        if is_before_code and line.strip().startswith('##') and not line.strip().startswith('###'):
            # ## を #### に変換
            new_line = line.replace('##', '####', 1)
            new_lines.append(new_line)
            modified = True
        else:
            new_lines.append(line)
    
    lines = new_lines
    
    # 2. 見出し階層の修正 (H2→H4 を H2→H3 に)
    new_lines = []
    heading_stack = []
    is_split_file = '_02' in file_path.name or '_03' in file_path.name
    
    for i, line in enumerate(lines):
        if line.startswith('#') and not line.startswith('```'):
            level = len(re.match(r'^#+', line).group())
            heading_text = line[level:].strip()
            
            # 分割ファイルの最初の見出しはそのまま
            if is_split_file and not heading_stack:
                new_lines.append(line)
                heading_stack.append(level)
                continue
            
            # H2→H4 のような2段階飛び越しを H2→H3 に修正
            if heading_stack and level > heading_stack[-1] + 1:
                new_level = heading_stack[-1] + 1
                new_line = '#' * new_level + ' ' + heading_text
                new_lines.append(new_line)
                modified = True
                
                while heading_stack and heading_stack[-1] >= new_level:
                    heading_stack.pop()
                heading_stack.append(new_level)
                continue
            
            # スタック更新
            while heading_stack and heading_stack[-1] >= level:
                heading_stack.pop()
            heading_stack.append(level)
        
        new_lines.append(line)
    
    if modified:
        new_content = '\n'.join(new_lines)
        file_path.write_text(new_content, encoding="utf-8")
    
    return modified

def main():
    print("最終SKILL修正開始...\n")
    
    fixed_count = 0
    
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        if final_fix(file_path):
            print(f"✓ {file_path.name}")
            fixed_count += 1
    
    print(f"\n完了: {fixed_count}ファイルを修正しました")

if __name__ == "__main__":
    main()
