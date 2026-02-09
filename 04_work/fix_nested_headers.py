# -*- coding: utf-8 -*-
"""
H2見出しの下に不要なH3（fix_hierarchy.pyで追加されたもの）がある場合、
H2をH3に書き換えて、不要なH3を削除するスクリプト。

Target Pattern:
## main.c（依存性注入の実行）
(解説文)
### main.c
#### main.c

Result:
### main.c（依存性注入の実行）
(解説文)
#### main.c
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def fix_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []
    
    skip_indices = set()
    
    # 全行スキャンしてパターンを探す
    for i in range(len(lines)):
        if i in skip_indices:
            continue
            
        line = lines[i]
        stripped = line.strip()
        
        # H2検出
        if stripped.startswith("## ") and not stripped.startswith("### "):
            # H2の内容
            h2_text = stripped.replace("## ", "").strip()
            
            # H2の下に、H3とH4が連続しているか探す
            # ただし間にある行数が多すぎると別のセクションかもしれないので、
            # 20行以内くらいで探す
            found_inserted_h3 = -1
            found_h4 = -1
            
            # 検索ループ
            for j in range(i + 1, min(i + 20, len(lines))):
                sub_line = lines[j].strip()
                
                # 別のH2が来たら終了
                if sub_line.startswith("## ") and not sub_line.startswith("### "):
                    break
                
                # H3検出
                if sub_line.startswith("### "):
                    # H3の中身が、H4と同じか、あるいはファイル名っぽいか
                    inserted_h3_text = sub_line.replace("### ", "").strip()
                    if found_inserted_h3 == -1:
                        found_inserted_h3 = j
                        inserted_h3_start_j = j
                    else:
                        # 2つ目のH3が来たら、前のH3はただの解説見出しかも？
                        # ここでは最初のH3をターゲットにする
                        pass

                # H4検出
                if sub_line.startswith("#### "):
                    h4_text = sub_line.replace("#### ", "").strip()
                    # H3とH4が近い位置にあるか？
                    # H3が見つかっており、それ以降であること
                    if found_inserted_h3 != -1:
                         # H3の内容とH4の内容が似ている、またはH2の内容にH4が含まれる
                         # 例: 
                         # H2: main.c(...)
                         # H3: main.c
                         # H4: main.c
                         
                         # あるいは単純に、fix_hierarchy.pyは H4の内容をそのままH3にしたので、
                         # H3 == H4 になっているはず（ただしH4はファイル名のみ）
                         
                         h3_text = lines[found_inserted_h3].replace("### ", "").strip()
                         
                         if h3_text == h4_text:
                             # パターン合致！
                             # アクション:
                             # 1. H2行(i) を "### " + h2_text に変更
                             lines[i] = "### " + h2_text
                             
                             # 2. H3行(found_inserted_h3) を削除（スキップリストに追加）
                             skip_indices.add(found_inserted_h3)
                             
                             # おしまい
                             break
            
        # 行追加（スキップ対象でなければ）
        if i not in skip_indices:
            new_lines.append(lines[i])

    # 保存
    new_content = "\n".join(new_lines)
    # 空行整理
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    
    if content != new_content:
        print(f"Fixed nested H2/H3/H4: {file_path.name}")
        file_path.write_text(new_content, encoding="utf-8")

def main():
    print("Fixing nested H2/H3/H4 headers...")
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        fix_file(file_path)
    print("Done.")

if __name__ == "__main__":
    main()
