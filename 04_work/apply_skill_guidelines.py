# -*- coding: utf-8 -*-
"""
SKILL.md & レビューガイドライン完全適用スクリプト
全ファイルを体系的に処理
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def apply_skill_guidelines(file_path: Path):
    """SKILL.mdとレビューガイドラインを適用"""
    content = file_path.read_text(encoding="utf-8")
    original_content = content
    modified = False
    
    # 1. Mermaid図の最適化
    # LR → TB 変換
    def convert_mermaid_lr_to_tb(match):
        mermaid_code = match.group(1)
        # graph LR → graph TB
        mermaid_code = re.sub(r'\bgraph\s+LR\b', 'graph TB', mermaid_code, flags=re.IGNORECASE)
        # flowchart LR → flowchart TB
        mermaid_code = re.sub(r'\bflowchart\s+LR\b', 'flowchart TB', mermaid_code, flags=re.IGNORECASE)
        return f"```mermaid\n{mermaid_code}```"
    
    content = re.sub(r'```mermaid\s*(.*?)```', convert_mermaid_lr_to_tb, content, flags=re.DOTALL)
    
    # 2. Mermaidタグのクリーンアップ (余計な属性削除)
    content = re.sub(r'```mermaid\s+style="[^"]*"', '```mermaid', content)
    content = re.sub(r'```mermaid\s+[^\n]+', '```mermaid', content)
    
    # 3. コードブロックの省略記号チェック
    # // ... や /* ... */ などの省略記号を検出
    省略記号パターン = [
        r'//\s*\.\.\.',
        r'/\*\s*\.\.\.\s*\*/',
        r'//\s*以下略',
        r'//\s*省略',
    ]
    
    for pattern in 省略記号パターン:
        if re.search(pattern, content):
            print(f"  [警告] {file_path.name}: 省略記号が検出されました")
    
    # 4. 見出し階層チェック
    lines = content.split('\n')
    heading_stack = []
    for i, line in enumerate(lines, 1):
        if line.startswith('#'):
            level = len(re.match(r'^#+', line).group())
            
            # H1がない状態でH2/H3が来ていないかチェック
            if level > 1 and not heading_stack:
                print(f"  [警告] {file_path.name}:L{i}: H1なしでH{level}が使用されています")
            
            # 階層が飛んでいないかチェック
            if heading_stack and level > heading_stack[-1] + 1:
                print(f"  [警告] {file_path.name}:L{i}: 見出し階層が飛んでいます (H{heading_stack[-1]} → H{level})")
            
            # スタック更新
            while heading_stack and heading_stack[-1] >= level:
                heading_stack.pop()
            heading_stack.append(level)
    
    # 5. コードブロックのフォーマットチェック
    # #### ファイル名 の直後に ```c があるかチェック
    code_blocks = re.finditer(r'####\s+([^\n]+)\n(.*?)```c', content, re.DOTALL)
    for match in code_blocks:
        filename = match.group(1).strip()
        between = match.group(2).strip()
        
        # 間に解説がない場合は警告
        if not between or len(between) < 20:
            print(f"  [情報] {file_path.name}: '{filename}' の解説が短い可能性があります")
    
    # 変更があった場合のみ保存
    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        modified = True
    
    return modified

def main():
    print("SKILL & レビューガイドライン完全適用開始...\n")
    
    modified_count = 0
    warning_count = 0
    
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        print(f"\n処理中: {file_path.name}")
        
        if apply_skill_guidelines(file_path):
            print(f"  ✓ 修正適用")
            modified_count += 1
        else:
            print(f"  - 変更なし")
    
    print(f"\n完了: {modified_count}ファイルを修正しました")

if __name__ == "__main__":
    main()
