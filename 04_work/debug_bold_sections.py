#!/usr/bin/env python3
"""デバッグ用: 特定箇所の内容を確認"""

import re
from pathlib import Path

chapter_dir = Path(__file__).parent.parent / "02_章別"
files = list(chapter_dir.glob("03_*.md"))

if files:
    text = files[0].read_text(encoding='utf-8')
    lines = text.split('\n')
    
    print(f"ファイル: {files[0].name}")
    print(f"総行数: {len(lines)}\n")
    
    # L283-285を確認
    for i in range(282, 286):
        if i < len(lines):
            line = lines[i]
            stripped = line.strip()
            is_bold = bool(re.match(r'^\*\*.*?\*\*:', stripped))
            print(f"L{i+1}: {repr(line[:100])}")
            print(f"  stripped: {repr(stripped[:80])}")
            print(f"  is_bold: {is_bold}")
            if i < len(lines) - 1:
                next_line = lines[i+1].strip()
                print(f"  next_line: {repr(next_line[:50])}")
            print()
