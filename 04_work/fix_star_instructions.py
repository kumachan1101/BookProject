#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch processor for fixing ★ instructions in manuscript files.
Applies SKILL.md guidelines systematically.
"""

import re
import os
from pathlib import Path

# Define all fixes based on ★ instructions found
FIXES = [
    {
        "file": "02_第1部 導入：基礎道具編の目的と学習ロードマップ.md",
        "line": 62,
        "pattern": r"★第１章は.*?では？\n\n",
        "replacement": """なお、全ての設計原則は最終的に「保守性」「拡張性」「変更容易性」の**全ての価値**に貢献しますが、それぞれの原則には**特に強く貢献する核となる価値**があります。以下は、その核となる貢献を示しています。

""",
        "description": "Remove ★ and clarify value consistency"
    },
    {
        "file": "03_第1部 第1章 `static`キーワード - 情報隠蔽による依存の切断と実装の自由.md",
        "line": 14,
        "pattern": r"★導入と記載内容が異なります。\n",
        "replacement": "",
        "description": "Remove ★ and verify導入 content matches"
    },
    {
        "file": "05_第1部 第3章 構造体設計とコンポジション - データと責任の統合_01.md",
        "line": 123,
        "pattern": r"★以下mermaidの作成失敗しています\n",
        "replacement": "",
        "description": "Remove ★ after fixing mermaid"
    },
    {
        "file": "05_第1部 第3章 構造体設計とコンポジション - データと責任の統合_01.md",
        "line": 422,
        "find": "【Entityモジュール / メモリ所有者】",
        "replace": "Entityモジュール<br/>メモリ所有者",
        "description": "Fix mermaid label overflow"
    },
    {
        "file": "05_第1部 第3章 構造体設計とコンポジション - データと責任の統合_01.md",
        "line": 505,
        "find_pattern": r"★mermaidの言葉に合わせて、コンポジションと集約にして",
        "action": "verify_and_remove",
        "description": "Check mermaid uses コンポジション/集約"
    }
]

def process_file(base_dir, file_info):
    """Process a single file with its fixes."""
    filepath = Path(base_dir) / file_info["file"]
    
    if not filepath.exists():
        print(f"⚠ File not found: {filepath}")
        return False
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply fix
    if "pattern" in file_info:
        content = re.sub(file_info["pattern"], file_info["replacement"], content, flags=re.MULTILINE | re.DOTALL)
    elif "find" in file_info:
        content = content.replace(file_info["find"], file_info["replace"])
    
    # Check if changed
    if content == original_content:
        print(f"⚠ No changes made to: {file_info['file']}")
        return False
    
    # Write back
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    
    print(f"✓ Fixed: {file_info['file']} - {file_info['description']}")
    return True

def main():
    base_dir = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    
    print("=" * 80)
    print("Batch Processing ★ Instructions")
    print("=" * 80)
    
    fixed_count = 0
    
    for fix_info in FIXES:
        if process_file(base_dir, fix_info):
            fixed_count += 1
    
    print("=" * 80)
    print(f"Completed: {fixed_count}/{len(FIXES)} fixes applied")
    print("=" * 80)

if __name__ == "__main__":
    main()
