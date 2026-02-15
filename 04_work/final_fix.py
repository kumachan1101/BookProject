import os
import re
from pathlib import Path

def fix_manuscript(file_path):
    print(f"Processing {file_path}")
    content = file_path.read_text(encoding="utf-8")
    
    # 1. YAMLフロントマターの削除 (--- ... ---)
    # 最初の --- から 次の --- までを削除
    if content.startswith("---"):
        parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            content = parts[2].strip() + "\n"
    
    # 2. 用語の統一
    content = content.replace("インターフェイス", "インターフェース")
    content = content.replace("V-Table", "VTable")
    
    # 3. リストの全角・半角スペース修正 (全角スペースを半角2つに)
    content = content.replace("　", "  ")
    
    # 4. ヘッダー周りの空行調整
    # H2, H3の前に空行がない場合は挿入、複数は1行に
    content = re.sub(r"\n+(##+ )", r"\n\n\1", content)
    
    # 5. 文章の末尾の不要なスペース削除
    content = re.sub(r" +$", "", content, flags=re.MULTILINE)
    
    # 6. Kindle向けの文脈改行 (特定のキーワードやパターンの後に空行を入れる)
    # 例: 「具体例:」の前に空行がない場合は挿入
    content = re.sub(r"([^\n])\n(具体例|狙い|ポイント|注意|重要)(\s*[:：*])", r"\1\n\n\2\3", content)
    
    # 7. 重複した空行（3行以上）を2行に
    content = re.sub(r"\n{3,}", "\n\n", content)

    file_path.write_text(content.lstrip(), encoding="utf-8")

def main():
    target_dir = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")
    for md_file in target_dir.glob("*.md"):
        fix_manuscript(md_file)

if __name__ == "__main__":
    main()
