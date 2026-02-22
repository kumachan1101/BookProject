
import glob
import os

def check_files():
    files = glob.glob(r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\*.md')
    print(f"Checking {len(files)} files...")
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i in range(len(lines) - 1):
            curr_line = lines[i].rstrip('\n')
            next_line = lines[i+1].rstrip('\n')
            
            # Check if current line is not empty, not a header, not a list item (heuristic)
            # and next line starts with **
            if curr_line and not curr_line.strip() == "":
                # Ignore if current line ends with 2 spaces
                if curr_line.endswith("  "):
                    continue
                # Ignore if next line is empty
                if next_line.strip() == "":
                    continue
                    
                # Check condition: Next line starts with **
                if next_line.strip().startswith("**") and not next_line.strip().startswith("-") and not next_line.strip().startswith("* "):
                    print(f"[POTENTIAL ISSUE] {os.path.basename(file_path)}:{i+1}")
                    print(f"  Curr: {curr_line}")
                    print(f"  Next: {next_line}")
                    print("-" * 20)

if __name__ == "__main__":
    check_files()
