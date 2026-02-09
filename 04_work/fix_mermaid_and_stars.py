# -*- coding: utf-8 -*-
"""
Mermaidエラー修正と★マーカー対応スクリプト
"""
import re
from pathlib import Path

# 対象ファイル
DIP_FILE = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_01.md")
ISP_FILE = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\15_第2部 第11章 インターフェース分離原則 (ISP) 不要な依存の排除とモジュール結合度の最小化_01.md")

def fix_mermaid_error(content):
    # graph TBがないMermaidブロックにgraph TBを追加
    # パターン: ```mermaid\n\s+ノード定義...
    # 修正: ```mermaid\n    graph TB\n    ノード定義...
    
    lines = content.split('\n')
    new_lines = []
    in_mermaid = False
    
    for i, line in enumerate(lines):
        if line.strip().startswith('```mermaid'):
            in_mermaid = True
            new_lines.append(line)
            # 次の行がgraph XXやsequenceDiagramで始まっていない場合、graph TBを追加
            if i + 1 < len(lines):
                next_line = lines[i+1].strip()
                if not (next_line.startswith('graph') or next_line.startswith('sequenceDiagram') or next_line.startswith('%%')):
                    new_lines.append('    graph TB')
            continue
            
        if line.strip().startswith('```') and in_mermaid:
            in_mermaid = False
            new_lines.append(line)
            continue
            
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def remove_star_markers(content):
    # ★で始まる行を削除
    lines = content.split('\n')
    new_lines = [line for line in lines if not line.strip().startswith('★')]
    return '\n'.join(new_lines)

def process_file(file_path):
    print(f"Processing {file_path.name}...")
    content = file_path.read_text(encoding='utf-8')
    
    # Mermaid修正
    content = fix_mermaid_error(content)
    
    # ★削除
    content = remove_star_markers(content)
    
    file_path.write_text(content, encoding='utf-8')
    print("Done.")

def main():
    if DIP_FILE.exists():
        process_file(DIP_FILE)
    if ISP_FILE.exists():
        process_file(ISP_FILE)

if __name__ == "__main__":
    main()
