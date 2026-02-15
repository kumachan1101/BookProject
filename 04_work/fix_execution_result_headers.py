import os
import re

TARGET_DIR = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"

def process_content(content):
    lines = content.split('\n')
    new_lines = []
    
    # Matches ### followed by anything containing "実行結果"
    # Example: ### 実行結果
    # Example: ### 実行結果（適用後）
    pattern = re.compile(r'^###\s+(.*実行結果.*)$')
    
    for line in lines:
        match = pattern.match(line.strip())
        if match:
             # Convert to ####
             # Keep the rest of the text
             new_lines.append(f"#### {match.group(1)}")
        else:
             new_lines.append(line)
             
    return '\n'.join(new_lines)


def main():
    modified_count = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = process_content(content)
                    
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        modified_count += 1
                        print(f"Fixed Execution Result level in: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                    
    print(f"Total files adjusted: {modified_count}")

if __name__ == "__main__":
    main()
