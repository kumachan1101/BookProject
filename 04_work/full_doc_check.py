# -*- coding: utf-8 -*-
"""
SKILL.mdとレビューガイドラインに基づく完全チェックツール
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def check_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors = []
    
    # 1. ★マーカーチェック
    for i, line in enumerate(lines, 1):
        if "★" in line:
            errors.append(f"Line {i}: ★マーカーが残っています: {line.strip()[:30]}...")

    # 2. Mermaid構文チェック
    in_mermaid = False
    mermaid_start_line = 0
    mermaid_content = []
    
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```mermaid"):
            in_mermaid = True
            mermaid_start_line = i
            mermaid_content = []
            continue
        
        if line.strip().startswith("```") and in_mermaid:
            in_mermaid = False
            # Mermaidブロックの中身をチェック
            text = "\n".join(mermaid_content).strip()
            if not (text.startswith("graph") or text.startswith("sequenceDiagram") or 
                    text.startswith("classDiagram") or text.startswith("flowchart") or
                    text.startswith("%%")):
                errors.append(f"Line {mermaid_start_line}: Mermaid図の種類定義(graph TB等)がありません")
            continue
            
        if in_mermaid:
            mermaid_content.append(line)

    # 3. コードブロック構造チェック (H3 -> 説明 -> H4 -> Code)
    # これは厳密にチェックするのは難しいが、簡易的に
    # 「コードブロックの直前に #### ファイル名 がない」ものを検出
    
    in_code = False
    last_h4_line = -100
    
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("#### "):
            last_h4_line = i
            
        if line.strip().startswith("```c") or line.strip().startswith("```cpp"):
            # 直前(空行除いて5行以内)にH4があるか
            # 簡単のため、行番号差でチェック
            if i - last_h4_line > 5:
                 # ただし、実行結果などは対象外とする場合もあるが、SKILLでは必須
                 # 今回は厳密にチェック
                 prev_lines = lines[max(0, i-6):i-1]
                 has_h4 = any(l.strip().startswith("#### ") for l in prev_lines)
                 if not has_h4:
                     errors.append(f"Line {i}: コードブロックの直前に '#### ファイル名' がありません")

    return errors

def main():
    print("ドキュメント完全チェック実行中...\n")
    
    total_errors = 0
    files_with_errors = 0
    
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        errors = check_file(file_path)
        if errors:
            print(f"■ {file_path.name}")
            for err in errors:
                print(f"  - {err}")
            print("")
            total_errors += len(errors)
            files_with_errors += 1
            
    print(f"\n完了: {files_with_errors}ファイルで計{total_errors}個の問題が見つかりました")

if __name__ == "__main__":
    main()
