import os
import re
import glob

def get_mermaid_blocks(content):
    return re.findall(r'(```mermaid[\s\S]*?```)', content)

def fix_text_part(text):
    # --- 1. 追加指定された見出しのH4化 (### -> ####) ---
    target_headers = [
        'システム概要', '目的', '機能', 'アーキテクチャ', '設計の意図', '実行結果'
    ]
    for header in target_headers:
        # 文頭（または改行直後）の ### にマッチ
        text = re.sub(r'(?m)^### ' + re.escape(header), r'#### ' + header, text)
    
    # ファイル名見出し ([name].[ch])
    text = re.sub(r'(?m)^### ([a-zA-Z0-9_\-.]+\.[ch])', r'#### \1', text)

    # --- 2. 注釈項目のリスト化 ---
    def fix_callout_items(match):
        header_tag = match.group(1)
        body = match.group(2)
        # 行頭の ### 項目名 を * **項目名**: に変換
        body = re.sub(r'(?m)^### \*\*([^*]+)\*\*[:：]?\s*', r'* **\1**: ', body)
        body = re.sub(r'(?m)^### ([^* \n][^\n]+)[:：]?\s*', r'* **\1**: ', body)
        # アイテムの結合分離
        body = re.sub(r'(\* \*\*[^*]+\*\*:[^\n*]+?) (\* \*\*)', r'\1\n\2', body)
        return header_tag + body

    target_tags = r'注目ポイント|読み方のガイド|達成される設計上のメリット|構成図|この図が示すもの|抽象（契約）|依存関係と隠蔽の構造|設計判断のポイント|設計の意図'
    text = re.sub(r'(##### (?:' + target_tags + r'))(\s*\n[\s\S]+?)(?=\n\n(?:####|##|#)|$)', fix_callout_items, text)

    return text

def restore_and_fix(original_content, target_content):
    # original_content (01_原稿) から Mermaid ブロックを抽出
    original_mermaids = get_mermaid_blocks(original_content)
    
    # target_content (02_章別) を Mermaid ブロックで分割
    parts = re.split(r'(```mermaid[\s\S]*?```)', target_content)
    
    fixed_parts = []
    mermaid_idx = 0
    for part in parts:
        if part.startswith('```mermaid'):
            if mermaid_idx < len(original_mermaids):
                # 原稿の Mermaid ブロックをそのまま採用（復元）
                fixed_parts.append(original_mermaids[mermaid_idx])
            else:
                # 原稿に存在しないブロック（考えにくいが）は維持
                fixed_parts.append(part)
            mermaid_idx += 1
        else:
            # テキスト部分は修正を適用
            fixed_parts.append(fix_text_part(part))
            
    return "".join(fixed_parts)

def main():
    source_dir = r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\01_原稿"
    target_dir = r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    
    target_files = glob.glob(os.path.join(target_dir, "*.md"))
    
    for target_path in target_files:
        basename = os.path.basename(target_path)
        if "03_" in basename:
            continue
            
        source_path = os.path.join(source_dir, basename)
        if not os.path.exists(source_path):
            print(f"Skipping (no source): {basename}")
            continue
            
        with open(source_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        with open(target_path, 'r', encoding='utf-8') as f:
            target_content = f.read()
            
        new_content = restore_and_fix(original_content, target_content)
        
        if target_content != new_content:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Restored & Fixed: {basename}")

if __name__ == "__main__":
    main()
