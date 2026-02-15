import re
from pathlib import Path

CHAPTER_DIR = Path(r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別")

def fix_all_execution_headers(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    original_content = content
    
    # regex to match ### 実行結果 followed by anything (like （適用前）) until end of line
    # captures the suffix in group 1 to preserve it
    pattern = r'^### (実行結果.*)$'
    
    # Replace with #### \1
    content = re.sub(pattern, r'#### \1', content, flags=re.MULTILINE)

    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        print(f"Fixed headers in: {file_path.name}")
        return True
    return False

def main():
    print("Fixing all '### Execution Result...' headers...")
    count = 0
    for file_path in sorted(CHAPTER_DIR.glob("*.md")):
        if fix_all_execution_headers(file_path):
            count += 1
    print(f"Finished. Modified {count} files.")

if __name__ == "__main__":
    main()
