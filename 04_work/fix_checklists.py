import os
import re
from pathlib import Path

target_dir = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

# Regex to match markdown checklists at the start of a line
# Examples: " [ ] ", "- [ ] ", "  * [ ] "
# Group 1 captures the leading whitespace
checklist_pattern = re.compile(r'^(\s*)[-*]?\s*\[[ \t]*\]\s+')

def fix_files():
    for filepath in target_dir.glob("*.md"):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        changed = False
        new_lines = []
        for line in lines:
            # 1. Checklist formatting
            # Only match if it actually modifies the line
            new_line = checklist_pattern.sub(r'\1* ', line)
            if new_line != line:
                line = new_line
                changed = True
            
            # 2. Fix specific stars
            if "★mermaidの説明と説明会っていますか？E1とE2とあるが、B1とB2が正しい？" in line:
                line = line.replace("★mermaidの説明と説明会っていますか？E1とE2とあるが、B1とB2が正しい？\n", "")
                changed = True
            elif "ここが設計の妙(★これは何て読むの？分かりやすい文章に変えて)です。" in line:
                line = line.replace("ここが設計の妙(★これは何て読むの？分かりやすい文章に変えて)です。", "ここが設計の要（かなめ）です。")
                changed = True
            
            # Also fix E1/E2 to B1/B2 in the text around the mermaid for 04_第1部 第2章
            if "実装側（E1/E2）" in line:
                line = line.replace("実装側（E1/E2）", "実装側（B1/B2）")
                changed = True
            if "E1を使うかE2を使うかを自由に選べます" in line:
                line = line.replace("E1を使うかE2を使うかを自由に選べます", "B1を使うかB2を使うかを自由に選べます")
                changed = True
            if "E1[具象実装 B1]" in line:
                line = line.replace("E1[具象実装 B1]", "B1[具象実装 B1]")
                changed = True
            if "E2[具象実装 B2]" in line:
                line = line.replace("E2[具象実装 B2]", "B2[具象実装 B2]")
                changed = True
            if "D -.->|\"実行時の結合\"| E1" in line:
                line = line.replace("E1", "B1")
                changed = True
            if "D -.->|\"実行時の結合\"| E2" in line:
                line = line.replace("E2", "B2")
                changed = True
            
            new_lines.append(line)
            
        if changed:
            with open(filepath, "w", encoding="utf-8", newline='\n') as f:
                f.writelines(new_lines)
            print(f"Fixed: {filepath.name}")

if __name__ == "__main__":
    fix_files()
