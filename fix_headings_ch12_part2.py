import sys
import os

filepath = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\16_第2部 第12章 依存性逆転原則（DIP）：抽象への依存とテスト容易性_02.md"

with open(filepath, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == "#### 具象への直接依存（違反状態）":
        new_lines.append("#### ❌ 原則適用前\n")
    else:
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.writelines(new_lines)
print("Finished standardizing headings in Chapter 12 Part 2.")
