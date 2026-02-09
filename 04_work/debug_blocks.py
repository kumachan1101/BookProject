# -*- coding: utf-8 -*-
from pathlib import Path

target_file = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_02.md")

def check_blocks():
    content = target_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    stack = []
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not stack:
                # ブロック開始
                stack.append(i)
                print(f"Line {i}: Block Start ({stripped})")
            else:
                # ブロック終了
                start_line = stack.pop()
                print(f"Line {i}: Block End (closed block from line {start_line})")
                
    if stack:
        print(f"\n[ERROR] Unclosed block starting at line {stack[0]}")
    else:
        print("\n[OK] All blocks check out.")

if __name__ == "__main__":
    check_blocks()
