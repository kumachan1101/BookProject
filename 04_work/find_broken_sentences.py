import os
import re
import glob

def find_broken_headings(content, filename):
    # 見出しの後に続く特定の助詞や動詞で始まる行を探す
    lines = content.split('\n')
    results = []
    
    # 接続の不自然な行の開始パターン
    # 「は」「が」「を」「に」「と」「で」「や」
    # 「を用いる」「によって」「により」「を学び」「を習得」など
    broken_starters = [
        'は', 'が', 'を', 'に', 'と', 'で', 'や', 
        'を用いる', 'によって', 'により', 'を学び', 'を習得', 'の採用は'
    ]
    
    for i in range(len(lines) - 1):
        line = lines[i].strip()
        next_line = lines[i+1].strip()
        
        # 見出し行かチェック
        if re.match(r'^#{2,4}\s+', line):
            # 次の行が空行を挟まずに、または1行の空行を挟んで、不自然な開始文字で始まっているか
            check_line = next_line
            if not check_line and i + 2 < len(lines):
                check_line = lines[i+2].strip()
                
            if any(check_line.startswith(s) for s in broken_starters):
                results.append((i+1, line, check_line))
                
    return results

def main():
    target_dir = r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
    files = glob.glob(os.path.join(target_dir, "*.md"))
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        broken = find_broken_headings(content, os.path.basename(file_path))
        if broken:
            print(f"--- {os.path.basename(file_path)} ---")
            for line_no, h, next_l in broken:
                print(f"Line {line_no}: {h} -> {next_l}")

if __name__ == "__main__":
    main()
