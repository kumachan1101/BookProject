import os
import re

TARGET_DIR = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"

def process_content(content):
    lines = content.split('\n')
    new_lines = []
    
    # Strict Regex for Filename detection:
    # Must end with typical code extension.
    # Supported: .c, .h, .cpp, .hpp, .py, .sh, .txt, .md, .json
    # Can contain dots, dashes, underscores, alphanumeric.
    
    # We want to change ANY Header level (#, ##, ###, #####, ######) to #### IF it matches filename.
    # EXCEPTION: If it is already ####, we keep it (no change).
    
    filename_pattern = re.compile(r'^(#+)\s+([\w\-\.]+\.(?:c|h|cpp|hpp|py|sh|txt|md|json))$', re.IGNORECASE)
    
    for line in lines:
        match = filename_pattern.match(line.strip())
        if match:
             current_level = match.group(1)
             filename = match.group(2)
             
             if len(current_level) != 4:
                 # Force to ####
                 new_lines.append(f"#### {filename}")
             else:
                 new_lines.append(line)
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
                        print(f"Fixed headers in: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                    
    print(f"Total files adjusted: {modified_count}")

if __name__ == "__main__":
    main()
