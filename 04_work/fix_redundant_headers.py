# -*- coding: utf-8 -*-
"""
冗長な見出し（## X の直後に ### X が来るなど）を修正するスクリプト
ユーザーの要望:
## 実行結果
### 実行結果
#### 実行結果
↓
### 実行結果
説明
#### 実行結果
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def fix_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []
    
    skip_next = False
    
    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue
            
        line = lines[i]
        stripped = line.strip()
        
        # ## 見出し を検出
        if stripped.startswith("## ") and not stripped.startswith("### "):
            header_text = stripped.replace("## ", "").strip()
            
            # 次の行（空行スキップ）を確認
            j = i + 1
            next_header_line_idx = -1
            while j < len(lines):
                if lines[j].strip() == "":
                    j += 1
                    continue
                if lines[j].strip().startswith("### " + header_text):
                    next_header_line_idx = j
                break
            
            if next_header_line_idx != -1:
                # 重複検出！
                # ## を削除し、### の行を生かす（ただし空行調整が必要かも）
                # いや、ユーザー要望は「### 実行結果」にしたいとのこと。
                # なので、現在の行（##）をスキップし、次の ### を採用すれば、結果的に H3 になる。
                # ただし、間の空行は維持したいか？
                # 単純にこの行を出力せず、次の ### までスキップするのは危険（間にテキストがないことは確認済みだが）。
                
                # 安全策: 現在の行を `### header_text` に書き換え、次の `### header_text` をスキップする。
                new_lines.append(f"### {header_text}")
                
                # 次の重複行を消すために、その行番号を記録してスキップ対象にする
                # ただしループ構造上、インデックスアクセスが面倒なので、
                # ここでは「次の有効行が重複しているなら、それを書き換えるのではなく、今の行を書き換えて、次の行を無視リストに入れる」
                
                # 簡易実装: linesリストを書き換えるのではなく、処理済みフラグを使う
                # ここで `j` (次の見出し行) を空行にする（new_linesに追加時に無視されるようにする）
                lines[next_header_line_idx] = "" 
                continue

        new_lines.append(line)

    # 保存
    new_content = "\n".join(new_lines)
    # 連続する空行を整理
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    
    if content != new_content:
        print(f"Fixed redundant headers: {file_path.name}")
        file_path.write_text(new_content, encoding="utf-8")

def main():
    print("Fixing redundant headers...")
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        fix_file(file_path)
    print("Done.")

if __name__ == "__main__":
    main()
