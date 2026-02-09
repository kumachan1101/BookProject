# -*- coding: utf-8 -*-
"""
SKILL.mdとレビューガイドラインに基づく最終監査スクリプト
"""
import re
from pathlib import Path

CHAPTER_DIR = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def check_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors = []
    
    # 1. コードブロックの閉じ忘れチェック
    code_block_count = 0
    for line in lines:
        if line.strip().startswith("```"):
            code_block_count += 1
    if code_block_count % 2 != 0:
        errors.append("コードブロックの開始・終了タグ(```)の数が一致しません（閉じ忘れの可能性）")

    in_code_block = False
    current_code_lines = 0
    code_start_line = 0
    
    # 見出し階層チェック用
    last_heading_level = 0
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # コードブロック内チェック
        if stripped.startswith("```"):
            # 言語指定がある場合は開始、なければ終了とみなす（簡易判定）
            # ただし ```c のように言語指定がある場合と、ただの ``` の場合がある
            # ここでは偶数・奇数で判定するのが確実だが、インラインで簡易的にやる
            if not in_code_block:
                in_code_block = True
                code_start_line = i
                current_code_lines = 0
                
                # Mermaidタグのクリーンさチェック
                if "mermaid" in stripped:
                    if len(stripped.replace("```mermaid", "").strip()) > 0:
                        errors.append(f"Line {i}: Mermaidタグの後ろに余計な文字があります: {stripped}")
            else:
                in_code_block = False
                # コードブロック行数チェック (100行以上は警告)
                if current_code_lines > 100:
                    errors.append(f"Line {code_start_line}: コードブロックが長すぎます({current_code_lines}行)。分割を検討してください。")
            continue
            
        if in_code_block:
            current_code_lines += 1
            # 省略記号のチェック
            if re.search(r"//\s*\.\.\.|/\*\s*\.\.\.\s*\*/|（以下略）|（中略）", stripped):
                errors.append(f"Line {i}: 省略記号が含まれています（完全なコードを出力してください）: {stripped}")
            continue

        # 見出し階層チェック
        if stripped.startswith("#"):
            level = len(stripped.split()[0])
            # H1(1) -> H2(2) -> H3(3) -> H4(4)
            # H2の次にH4が来るのはNG (H3飛ばし)
            if level == 4 and last_heading_level == 2:
                errors.append(f"Line {i}: H2見出しの直後にH4見出しが来ています（H3を飛ばしています）")
            
            if level <= 4: # H5以降は自由度高いのでチェックしない
                last_heading_level = level

        # リンク形式チェック (内部リンクのみ)
        # [text](filename.md) 形式はNG -> [[filename]] 推奨
        # ただし http リンクは除外
        link_match = re.search(r"\[.*?\]\((.*?)\)", stripped)
        if link_match:
            url = link_match.group(1)
            if not url.startswith("http") and not url.startswith("#") and ".md" in url:
                errors.append(f"Line {i}: 標準Markdownリンクが使われています（WikiLinks推奨）: {stripped}")

        # Callout記法チェック
        if stripped.startswith(">"):
            if re.search(r"> \s+\[!NOTE\]", stripped): # スペース過多
                errors.append(f"Line {i}: Callout記法のスペースが多すぎます: {stripped}")
            if re.search(r"> \[!NOTE\]:", stripped): # コロン不要
                errors.append(f"Line {i}: Callout記法に不要なコロンがあります: {stripped}")

    return errors

def main():
    print("最終コンプライアンス監査を実行中...\n")
    
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
