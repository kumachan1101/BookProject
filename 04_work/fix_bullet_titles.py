"""
箇条書きの「タイトル部分」と「本文」が分断されているパターンを修正するスクリプト。

対象パターン:
*   **タイトル**
    本文テキスト

修正後:
*   **タイトル**　本文テキスト

また、行末の不要なスペース（半角/全角）も除去する。
"""

import re
import glob
import os

TARGET_DIR = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"

def fix_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    original = content

    # ─── 修正1: 箇条書きタイトルと次行の本文が分断されているパターン ───
    # * で始まる行が **...** で終わり、次行がインデント付きテキストのケース
    # 例:
    #   *   **コンパイル依存の最小化**
    #       `static`にされた...
    # ↓
    #   *   **コンパイル依存の最小化**　`static`にされた...
    pattern = re.compile(
        r'^(\s*\*+\s+\*\*[^*]+\*\*)\n'   # グループ1: *   **タイトル**
        r'(\s+)(\S.+)$',                  # グループ3: インデントされた本文行（任意の文字から始まる）
        re.MULTILINE
    )

    def merge_title_body(m):
        title_line = m.group(1)
        body_text = m.group(3).strip()
        return f"{title_line}\u3000{body_text}"

    content = pattern.sub(merge_title_body, content)

    # ─── 修正2: 行末の不要な半角スペース（1個以上）を除去 ───
    content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"修正: {os.path.basename(filepath)}")
    else:
        print(f"変更なし: {os.path.basename(filepath)}")

def main():
    md_files = glob.glob(os.path.join(TARGET_DIR, "*.md"))
    print(f"{len(md_files)} ファイルを処理します...\n")
    for fp in sorted(md_files):
        fix_file(fp)
    print("\n完了。")

if __name__ == "__main__":
    main()
