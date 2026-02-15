#!/usr/bin/env python3
"""
連続する**で始まる行の間に空行を挿入するスクリプト

例:
**処理の内容:** ...
**設計的意図:** ...
**評価:** ...

↓

**処理の内容:** ...

**設計的意図:** ...

**評価:** ...
"""

import re
from pathlib import Path

def add_blank_lines_between_bold_sections(text: str) -> str:
    """連続する**で始まる行の後に空行を挿入
    
    ロジック:
    - **text:**形式の行を見つける (例: **処理の内容:** ...)
    - その行の後に空行を挿入(次の行が既に空行の場合は除く)
    - ただし、ファイルの最後の行は除外
    """
    lines = text.split('\n')
    result = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        # **で始まり、:**で終わるパターン (例: **処理の内容:** ...)
        # 実際の形式は **text:** (コロンが**の前)
        is_bold_section = bool(re.match(r'^\*\*[^*]+:\*\*', stripped))
        
        result.append(line)
        
        # boldセクションの行の後に空行を挿入
        if is_bold_section and i < len(lines) - 1:
            # 次の行を確認
            next_line = lines[i+1].strip()
            
            # 次の行が空行でない場合のみ空行を挿入
            if next_line:
                result.append('')  # 空行を追加
    
    return '\n'.join(result)


def process_file(file_path: Path):
    """ファイルを処理"""
    print(f"処理中: {file_path.name}")
    
    # ファイル読み込み
    text = file_path.read_text(encoding='utf-8')
    
    # 変換前の**...**:の数をカウント
    before_count = len(re.findall(r'^\*\*[^*]+\*\*:', text, re.MULTILINE))
    
    # 変換
    new_text = add_blank_lines_between_bold_sections(text)
    
    # 変更があった場合のみ書き込み
    if new_text != text:
        file_path.write_text(new_text, encoding='utf-8')
        print(f"  ✓ 修正完了 ({before_count}箇所のboldセクション)")
    else:
        print(f"  - 変更なし")


def main():
    """メイン処理"""
    chapter_dir = Path(__file__).parent.parent / "02_章別"
    
    if not chapter_dir.exists():
        print(f"エラー: {chapter_dir} が見つかりません")
        return
    
    # 全mdファイルを処理
    md_files = sorted(chapter_dir.glob("*.md"))
    
    print(f"\n{len(md_files)}個のファイルを処理します\n")
    
    for md_file in md_files:
        process_file(md_file)
    
    print(f"\n完了: {len(md_files)}ファイルを処理しました")


if __name__ == "__main__":
    main()
