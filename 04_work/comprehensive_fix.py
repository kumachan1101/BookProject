# -*- coding: utf-8 -*-
"""
Mermaidエラーとコードブロック見出し欠落の包括的修正スクリプト
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def fix_file(file_path: Path):
    print(f"Processing {file_path.name}...")
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []
    
    in_mermaid = False
    mermaid_block = []
    mermaid_start_idx = -1
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # --- Mermaid修正 ---
        if line.strip().startswith("```mermaid"):
            new_lines.append(line)
            # 次の行をチェック
            if i + 1 < len(lines):
                next_line = lines[i+1].strip()
                # 既に有効な宣言があれば何もしない
                if not (next_line.startswith("graph") or 
                        next_line.startswith("sequenceDiagram") or 
                        next_line.startswith("classDiagram") or 
                        next_line.startswith("flowchart") or
                        next_line.startswith("%%")):
                    # sequenceDiagramっぽいキーワードがあるかチェック
                    if "participant" in content[content.find("```mermaid", 0)+10 : content.find("```", content.find("```mermaid", 0)+10)]: 
                        # 簡易チェック: participantがあればsequenceDiagramかも？
                        # しかしブロックごとの判定じゃないと誤爆する
                        pass
                    
                    # ブロックの中身を先読みして判定
                    is_sequence = False
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith("```"):
                        if "participant" in lines[j] or "->" in lines[j] or "-->>" in lines[j]:
                             # graphでも -> は使うが、participantはsequence特有
                             if "participant" in lines[j]:
                                 is_sequence = True
                        j += 1
                    
                    if is_sequence:
                        new_lines.append("    sequenceDiagram")
                    else:
                        new_lines.append("    graph TB")
            i += 1
            continue

        # --- コードブロック見出し補完 ---
        if line.strip().startswith("```c") or line.strip().startswith("```cpp") or line.strip().startswith("```bash"):
            # 直前の行（空行スキップ）を確認
            # new_linesの後ろから遡る
            headers_found = False
            lookback_idx = len(new_lines) - 1
            
            # 空行をスキップして直前のテキスト行を探す
            while lookback_idx >= 0:
                prev = new_lines[lookback_idx].strip()
                if prev == "":
                    lookback_idx -= 1
                    continue
                
                if prev.startswith("####"):
                    headers_found = True
                
                # 直前の行が「#### 実行結果」などを意図したテキストかもしれない
                # しかし、ここでは安全のため、H4がないなら挿入する
                break
            
            if not headers_found:
                # 挿入すべき見出しを決定
                heading_text = "#### コード例" # デフォルト
                
                # 直前の文章から推測（簡易的）
                search_range = 5
                context_text = ""
                for k in range(max(0, len(new_lines)-search_range), len(new_lines)):
                    context_text += new_lines[k]
                
                if "実行結果" in context_text:
                    heading_text = "#### 実行結果"
                elif "ヘッダ" in context_text or ".h" in context_text:
                     # ファイル名が特定できないので汎用的に
                     pass 
                
                # 空行を挟んで見出しを追加
                if new_lines and new_lines[-1].strip() != "":
                    new_lines.append("")
                new_lines.append(heading_text)
                
        new_lines.append(line)
        i += 1

    # 保存
    new_content = "\n".join(new_lines)
    # 末尾の改行確保
    if not new_content.endswith("\n"):
        new_content += "\n"
        
    file_path.write_text(new_content, encoding="utf-8")

def main():
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        fix_file(file_path)
    print("All files processed.")

if __name__ == "__main__":
    main()
