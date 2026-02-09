import re
import sys

# ファイルを読み込む
with open(r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\08_第1部 第6章 エラーハンドリングパターン - 堅牢な契約_01.md', 'r', encoding='utf-8') as f:
    content = f.read()

# パターン: "#### ファイル名 (説明)" の後に続く ```c を探す
# ファイル名を抽出して、コードブロックの直前に #### ファイル名 を追加

# まず、全ての #### セクションヘッダーとそれに続くコードブロックを見つける
pattern = r'(#### ([^\r\n]+?)(?:\s*\(.*?\))?\s*\r?\n\r?\n)((?:.*?\r?\n)*?)(\r?\n```c\r?\n)'

def add_code_caption(match):
    header = match.group(1)  # "#### user.h (抽象契約)\n\n"
    filename_line = match.group(2)  # "user.h (抽象契約)"
    explanation = match.group(3)  # 解説文
    code_start = match.group(4)  # "\n```c\n"
    
    # ファイル名を抽出 (括弧の前まで)
    filename = filename_line.split('(')[0].strip() if '(' in filename_line else filename_line.strip()
    
    # コードブロックの直前に #### ファイル名 を追加
    return header + explanation + f'\r\n#### {filename}\r\n' + code_start

# 置換を実行
modified_content = re.sub(pattern, add_code_caption, content, flags=re.MULTILINE)

# 結果を書き込む
with open(r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\08_第1部 第6章 エラーハンドリングパターン - 堅牢な契約_01.md', 'w', encoding='utf-8') as f:
    f.write(modified_content)

print("完了: コードキャプションを追加しました")
