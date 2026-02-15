import re
from pathlib import Path

TARGET_DIR = Path(r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def fix_headers_in_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    original_content = content
    
    # 1. Fix Filename Headers: ### filename.ext -> #### filename.ext
    # Regex looks for ### followed by space and a typical filename pattern
    # It avoids changing other H3 headers that are not filenames
    filename_pattern = r'^### (.*\.(c|h|py|cpp|js|ts|html|css|json|xml|yaml|txt|md))$'
    content = re.sub(filename_pattern, r'#### \1', content, flags=re.MULTILINE)

    # 2. Fix Execution Result Headers: ### 実行結果 -> #### 実行結果
    execution_pattern = r'^### 実行結果$'
    content = re.sub(execution_pattern, r'#### 実行結果', content, flags=re.MULTILINE)

    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        print(f"Fixed headers in: {file_path.name}")
        return True
    return False

def main():
    print("Starting header fix (### -> ####)...")
    count = 0
    for file_path in TARGET_DIR.glob("*.md"):
        if fix_headers_in_file(file_path):
            count += 1
    print(f"Finished. Modified {count} files.")

if __name__ == "__main__":
    main()
