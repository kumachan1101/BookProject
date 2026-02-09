# -*- coding: utf-8 -*-
"""
H3とH4の整合性を修正するスクリプト
H3にファイル名が含まれている場合、続くH4の「コード例」をそのファイル名に置換する。
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def extract_filename(h3_text):
    # マークダウン強調などを除去
    clean_text = h3_text.replace("**", "").replace("*", "").replace("`", "")
    
    # 拡張子を持つ単語を探す
    match = re.search(r'[\w\-\.]+\.(c|h|cpp|hpp|py|sh|txt)', clean_text, re.IGNORECASE)
    if match:
        return match.group(0)
    return None

def fix_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []
    
    current_filename = None
    
    for line in lines:
        line_stripped = line.strip()
        
        # H3: ### ...
        if line_stripped.startswith("### ") and not line_stripped.startswith("#### "):
            filename = extract_filename(line_stripped)
            if filename:
                current_filename = filename
            else:
                current_filename = None # ファイル名が見つからない場合はリセット
        
        # H4: #### コード例
        if line_stripped == "#### コード例" and current_filename:
            new_lines.append(f"#### {current_filename}")
        else:
            new_lines.append(line)
            
    # 保存
    new_content = "\n".join(new_lines)
    # 元が末尾改行ありなら維持
    if content.endswith("\n") and not new_content.endswith("\n"):
        new_content += "\n"
        
    if new_content != content:
        print(f"Fixed: {file_path.name}")
        file_path.write_text(new_content, encoding="utf-8")

def main():
    print("Fixing H3/H4 mismatches...")
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        fix_file(file_path)
    print("Done.")

if __name__ == "__main__":
    main()
