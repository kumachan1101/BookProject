import os
import re
import glob

def fix_text_part(text):
    # --- 1. 追加指定された見出しのH4化 (### -> ####) ---
    target_headers = [
        'システム概要', '目的', '機能', 'アーキテクチャ', '設計の意図', '実行結果'
    ]
    for header in target_headers:
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

def surgical_fix_file(content):
    # Mermaidブロックを保護するために分割
    parts = re.split(r'(```mermaid[\s\S]*?```)', content)
    
    fixed_parts = []
    for i, part in enumerate(parts):
        if part.startswith('```mermaid'):
            # Mermaidブロックは1文字も変えずにそのまま保持
            fixed_parts.append(part)
        else:
            # それ以外のテキスト部分のみ修正
            fixed_parts.append(fix_text_part(part))
            
    return "".join(fixed_parts)

def main():
    target_dir = r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    files = glob.glob(os.path.join(target_dir, "*.md"))
    
    for file_path in files:
        if "03_" in os.path.basename(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = surgical_fix_file(content)
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed: {os.path.basename(file_path)}")

if __name__ == "__main__":
    main()
