import re
from pathlib import Path

# Paths to the specific files that failed
files_to_fix = [
    Path(r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\12_第2部 第8章 単一責任原則 (SRP) 変更の軸を明確にする設計指針_01.md"),
    Path(r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\12_第2部 第8章 単一責任原則 (SRP) 変更の軸を明確にする設計指針_02.md")
]

def fix_stubborn_headers(file_path: Path):
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    content = file_path.read_text(encoding="utf-8")
    original_content = content
    
    # Use a looser regex that allows for trailing whitespace
    # and maybe even leading whitespace? No, markdown headers are usually at start of line.
    # But let's allow for possible trailing spaces or tabs.
    content = re.sub(r'^### 実行結果\s*$', '#### 実行結果', content, flags=re.MULTILINE)

    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        print(f"Fixed headers in: {file_path.name}")
    else:
        print(f"No changes made to: {file_path.name}")

if __name__ == "__main__":
    for p in files_to_fix:
        fix_stubborn_headers(p)
