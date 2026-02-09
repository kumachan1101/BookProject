# -*- coding: utf-8 -*-
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def check_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors = []
    
    current_h3_filename = None
    
    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()
        
        # H3: ### ファイル名 (の抽出)
        if line_stripped.startswith("### ") and not line_stripped.startswith("#### "):
            # ファイル名っぽいもの（拡張子がある、または特定のキーワード）を抽出
            # 例: ### main.c または ### main.c (詳細)
            # 簡易的に最初の単語を取る
            parts = line_stripped.replace("###", "").strip().split('（')
            candidate = parts[0].strip()
            if "." in candidate or candidate.lower().endswith("file"):
                 current_h3_filename = candidate
            else:
                 current_h3_filename = None
        
        # H4: #### ファイル名
        if line_stripped.startswith("#### "):
            h4_text = line_stripped.replace("####", "").strip()
            
            # 直近のH3と一致しているか確認
            # コード例 や 実行結果 は除外
            if h4_text in ["コード例", "実行結果", "ビルドと実行"]:
                continue
               
            # H3があるのに、H4が全然違う、あるいはH4が「コード例」になってしまっているケースを検出したい
            pass

        # コードブロックの直前チェック
        if line_stripped.startswith("```c") or line_stripped.startswith("```cpp"):
            # 直前のH4を探す
            found_h4 = None
            for k in range(i-2, max(-1, i-10), -1):
                prev = lines[k].strip()
                if prev.startswith("#### "):
                    found_h4 = prev.replace("####", "").strip()
                    break
            
            if found_h4:
                # H3でファイル名が指定されているのに、H4が「コード例」になっている場合
                if current_h3_filename and found_h4 == "コード例":
                    errors.append(f"Line {i}: H3で '{current_h3_filename}' が指定されていますが、H4が 'コード例' になっています。")

    return errors

def main():
    print("H3/H4 整合性チェック中...\n")
    
    total_errors = 0
    
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        errors = check_file(file_path)
        if errors:
            print(f"■ {file_path.name}")
            for err in errors:
                print(f"  - {err}")
            total_errors += len(errors)
            
    print(f"\n完了: {total_errors}個の問題が見つかりました")

if __name__ == "__main__":
    main()
