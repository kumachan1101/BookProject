# -*- coding: utf-8 -*-
"""
見出し階層とコード省略記号の自動修正スクリプト
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def fix_heading_hierarchy(file_path: Path):
    """見出し階層の問題を修正"""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    modified = False
    
    # H1→H4の飛び越しを H1→H2→H3→H4 に修正
    # #### (H4) を ### (H3) に変換 (コードブロック直前の見出しのみ)
    new_lines = []
    for i, line in enumerate(lines):
        # #### で始まり、その後に```cがある場合
        if line.startswith('#### ') and i + 1 < len(lines):
            # 次の行または数行後に```cがあるかチェック
            is_code_heading = False
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip().startswith('```c'):
                    is_code_heading = True
                    break
                if lines[j].strip() and not lines[j].strip().startswith('```'):
                    break
            
            if is_code_heading:
                # コードブロック直前の見出しはそのまま維持
                new_lines.append(line)
            else:
                # それ以外のH4はH3に変換
                new_lines.append('###' + line[4:])
                modified = True
        else:
            new_lines.append(line)
    
    if modified:
        content = '\n'.join(new_lines)
        file_path.write_text(content, encoding="utf-8")
    
    return modified

def fix_code_omissions(file_path: Path):
    """コードブロック内の省略記号を検出して報告"""
    content = file_path.read_text(encoding="utf-8")
    
    # コードブロック内の省略記号を検出
    code_blocks = re.finditer(r'```c\s*(.*?)```', content, re.DOTALL)
    
    omissions = []
    for match in code_blocks:
        code = match.group(1)
        if re.search(r'//\s*\.\.\.', code) or re.search(r'/\*\s*\.\.\.\s*\*/', code):
            omissions.append({
                'start': match.start(),
                'code_snippet': code[:100]
            })
    
    return omissions

def main():
    print("見出し階層とコード省略記号の修正開始...\n")
    
    heading_fixed = 0
    omission_files = []
    
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        # 見出し階層修正
        if fix_heading_hierarchy(file_path):
            print(f"✓ {file_path.name}: 見出し階層を修正")
            heading_fixed += 1
        
        # 省略記号チェック
        omissions = fix_code_omissions(file_path)
        if omissions:
            omission_files.append({
                'file': file_path.name,
                'count': len(omissions)
            })
    
    print(f"\n見出し階層修正: {heading_fixed}ファイル")
    
    if omission_files:
        print(f"\nコード省略記号検出:")
        for item in omission_files:
            print(f"  - {item['file']}: {item['count']}箇所")
        print("\n  ⚠️ これらのファイルは手動で完全なコードに修正する必要があります")
    else:
        print("\nコード省略記号: 検出なし ✓")

if __name__ == "__main__":
    main()
