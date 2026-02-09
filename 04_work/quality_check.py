import sys
from pathlib import Path
import re

TARGET_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def check_file(file_path):
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors = []
    
    in_code_block = False
    block_start_line = 0
    language = ""
    
    # 状態管理
    # code_blocks: list of (start_line, end_line, language)
    
    # 簡易的な行スキャン
    for i, line in enumerate(lines):
        line_num = i + 1
        stripped = line.strip()
        
        # 1. 禁則文字チェック
        if "★" in line:
            errors.append(f"Line {line_num}: Contains '★' marker")
        
        # 2. 省略記号チェック (厳密には難しいが、典型的なものを抽出)
        # if "// ..." in line or "/* ... */" in line:
        #     errors.append(f"Line {line_num}: Potential code omission marker found")
            
        # 3. Mermaidチェック
        if stripped.startswith("```mermaid"):
            # 次の行以降を少し読んで graph LR をチェック
            # (これは簡易チェック)
            pass

        # 4. コードブロック構造チェック
        if stripped.startswith("```"):
            # 言語指定の取得 (```c, ```pythonなど)
            current_lang_tag = stripped[3:].strip()
            
            if in_code_block:
                # ブロック終了
                if stripped == "```":
                    in_code_block = False
                    
                    # Graph LR check logic inside block could go here if managed
                else:
                    # ネストされたブロックなどの異常
                    # errors.append(f"Line {line_num}: Nested code block or missing close tag?")
                    # Markdownでは ``` の中で ``` は書かないはず
                    pass
            else:
                # ブロック開始
                in_code_block = True
                block_start_line = line_num
                language = current_lang_tag
                
                # 対象言語のみチェック (textやshellは除外する場合もあるが、原則すべてチェック)
                # 特に c, cpp, python, h, mermaid は対象
                target_langs = ["c", "cpp", "python", "h", "mermaid"]
                
                if language in target_langs or (language == "" and "mermaid" not in language): 
                    # 言語指定なしも警告対象だが、一旦説明文の構造をチェック
                    
                    # 直前の行（空行スキップ）を取得
                    pre_code_index = i - 1
                    while pre_code_index >= 0 and not lines[pre_code_index].strip():
                        pre_code_index -= 1
                    
                    if pre_code_index >= 0:
                        prev_line = lines[pre_code_index].strip()
                        
                        # ルールA: コードブロックの直前は #### ファイル名 であるべき
                        # Mermaidの場合は図の説明など
                        
                        if language == "mermaid":
                            # Mermaidは図表なので、必ずしも #### ファイル名 ではないが
                            # 図の説明文があるべき
                            pass
                        elif language in ["c", "cpp", "python", "h"]:
                            is_result_block = "実行結果" in prev_line or "出力" in prev_line or "Execution Result" in prev_line
                            
                            # #### ヘッダがあるか確認
                            if not prev_line.startswith("#### "):
                                if not is_result_block:
                                    errors.append(f"Line {line_num}: Code block '{language}' missing '#### filename' header. Found: '{prev_line}'")
                            else:
                                # #### ヘッダがある場合、そのさらに前を確認（解説があるか）
                                header_index = pre_code_index
                                pre_header_index = header_index - 1
                                while pre_header_index >= 0 and not lines[pre_header_index].strip():
                                    pre_header_index -= 1
                                
                                if pre_header_index >= 0:
                                    pre_header_line = lines[pre_header_index].strip()
                                    
                                    # 解説がなく見出しが連続している場合
                                    if pre_header_line.startswith("#"):
                                        errors.append(f"Line {header_index+1}: '####' header immediately follows another header ('{pre_header_line}'). Missing detailed explanation.")
                                    # 解説がなくコードブロックが連続している場合（前のブロック閉）
                                    elif pre_header_line.startswith("```"):
                                        errors.append(f"Line {header_index+1}: '####' header immediately follows another code block. Missing detailed explanation between blocks.")

    # 全文検索でのチェック
    if re.search(r'graph\s+LR', text):
        errors.append("Global: Contains 'graph LR' (should be TB)")
        
    return errors

def main():
    if not TARGET_DIR.exists():
        print(f"Directory not found: {TARGET_DIR}")
        return

    files = sorted(TARGET_DIR.glob("*.md"))
    total_errors = 0
    error_files = 0
    
    print(f"Auditing {len(files)} files in {TARGET_DIR.name}...\n")
    
    for f in files:
        errs = check_file(f)
        if errs:
            error_files += 1
            print(f"[{f.name}]")
            for e in errs:
                print(f"  {e}")
            total_errors += len(errs)
            print("") # Empty line
            
    print("-" * 40)
    print(f"Total Errors: {total_errors}")
    print(f"Files with Errors: {error_files} / {len(files)}")
    
    if total_errors == 0:
        print("\nSUCCESS: All files passed the quality check.")

if __name__ == "__main__":
    main()
