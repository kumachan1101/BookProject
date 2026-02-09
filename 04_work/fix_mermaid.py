# -*- coding: utf-8 -*-
"""
Mermaid図修正スクリプト: subgraph単独使用を修正
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def fix_mermaid_diagrams(file_path: Path):
    """Mermaid図のsubgraph単独使用を修正"""
    content = file_path.read_text(encoding="utf-8")
    original = content
    
    # ```mermaid ... ``` ブロックを検出
    def fix_mermaid_block(match):
        mermaid_code = match.group(1)
        
        # 既にgraph/flowchart宣言がある場合はスキップ
        if re.search(r'^\s*(graph|flowchart|classDiagram|sequenceDiagram|mindmap)\s+', mermaid_code, re.M):
            return match.group(0)
        
        # subgraphで始まる場合、graph TBを追加
        if re.search(r'^\s*subgraph\s+', mermaid_code, re.M):
            # インデントを保持しながらgraph TBを追加
            lines = mermaid_code.split('\n')
            new_lines = ['graph TB']
            
            # 既存の行をインデント
            for line in lines:
                if line.strip():
                    new_lines.append('  ' + line)
                else:
                    new_lines.append(line)
            
            new_mermaid = '\n'.join(new_lines)
            return f'```mermaid\n{new_mermaid}\n```'
        
        return match.group(0)
    
    # 全てのMermaidブロックを修正
    content = re.sub(r'```mermaid\s*\n(.*?)\n```', fix_mermaid_block, content, flags=re.S)
    
    if content != original:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    print("Mermaid図修正開始...\n")
    
    fixed_count = 0
    
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        if fix_mermaid_diagrams(file_path):
            print(f"✓ {file_path.name}")
            fixed_count += 1
    
    print(f"\n完了: {fixed_count}ファイルを修正しました")

if __name__ == "__main__":
    main()
