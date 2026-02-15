import os
import re
import glob

def rescue_file(content):
    # Mermaidブロックを保護
    parts = re.split(r'(```mermaid[\s\S]*?```)', content)
    
    fixed_parts = []
    for i, part in enumerate(parts):
        if part.startswith('```mermaid'):
            # Mermaidはそのまま
            fixed_parts.append(part)
        else:
            # テキスト部分の誤変換を戻す
            text = part
            # パターン: * **filename.h**: descriptions...
            # 見出し #### filename.h\n\ndescriptions... に戻す
            # 漢字のコロンにも対応
            text = re.sub(r'(?m)^\* \*\*([a-zA-Z0-9_\-.]+\.[ch])\*\*[:：]?\s*(.*)', r'#### \1\n\n\2', text)
            
            # 連続する空行を整理 (#### の前後に空行を入れる)
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            fixed_parts.append(text)
            
    return "".join(fixed_parts)

def main():
    target_dir = r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    files = glob.glob(os.path.join(target_dir, "*.md"))
    
    for file_path in files:
        if "03_" in os.path.basename(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = rescue_file(content)
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Rescued: {os.path.basename(file_path)}")

if __name__ == "__main__":
    main()
