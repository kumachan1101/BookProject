import os
import re

# Target directory
TARGET_DIR = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"

# Generic phrases to identify the blocks to remove
GENERIC_PHRASES = [
    "ヘッダで定義されたインターフェースの具体的な実装を行います",
    "モジュールの公開インターフェース定義を行います",
    "実装詳細を隠蔽し、外部には必要な契約（API）のみを公開することで、結合度を下げます",
    "変更が発生しても、このファイル内のみに影響を留めることができます",
    "インターフェースと実装が分離され、高い保守性が確保されています",
    "内部データや詳細ロジックをこのファイル内に閉じ込め（カプセル化）、外部からの直接アクセスを防ぎます",
    "コードの処理内容を示します", # Also saw this in 12_01.md (Line 543)
    "適切に責務の分離を行っています", 
    "可読性と保守性に優れた実装です"
]

def is_generic_block(content_chunk):
    """Checks if a chunk of text contains generic phrases."""
    matches = 0
    for phrase in GENERIC_PHRASES:
        if phrase in content_chunk:
            matches += 1
    return matches >= 2 # Require at least 2 matches to be sure

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # Pattern to capture:
    # (Optional Header)
    # **処理の内容:** ...
    # ...
    # **評価:** ...
    
    # We look for the "Processing Content" to "Evaluation" block.
    # Regex breakdown:
    # (?P<header>(?:^|\n)#{1,6} [^\n]+\n\s*)?  --> Optional preceding header (group 'header')
    # (?P<block>\*\*処理の内容:\*\*.*?\*\*評価:\*\*.*?\n(?:\s*\n)?) --> The block itself (group 'block')
    
    # Note: Regex in python is greedy by default, but .*? is non-greedy.
    # We need to handle multi-line dot matching.
    
    pattern = re.compile(
        r'(?P<header>(?:^|\n)#{1,6} [^\n]+\n\s*)?' 
        r'(?P<block>\*\*処理の内容:\*\*.*?\*\*評価:\*\*.*?(?:\n|$))',
        re.DOTALL
    )

    new_content = content
    
    # We iterate finding matches. 
    # Because we are modifying the string, it's safer to rebuild it or use re.sub with a callback.
    
    def replacement(match):
        header = match.group('header')
        block = match.group('block')
        
        if is_generic_block(block):
            print(f"  Removing generic block in {os.path.basename(filepath)}")
            if header:
                print(f"    Also removing header: {header.strip()}")
                return "" # Remove both
            else:
                return "" # Remove block only
        else:
            return match.group(0) # Keep original
            
    new_content = pattern.sub(replacement, content)
    
    if new_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                if process_file(path):
                    count += 1
    print(f"Processed {count} files.")

if __name__ == "__main__":
    main()
