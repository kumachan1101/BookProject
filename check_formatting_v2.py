
import glob
import os

def check_files():
    files = glob.glob(r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\*.md')
    found_issues = False
    
    with open('formatting_issues.txt', 'w', encoding='utf-8') as report:
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except Exception as e:
                report.write(f"Error reading {file_path}: {e}\n")
                continue
                
            for i in range(len(lines) - 1):
                curr_line = lines[i].rstrip('\n') # Keep spaces at end to check
                next_line = lines[i+1].strip() # Check content
                
                # Condition:
                # 1. Current line has content
                # 2. Current line does NOT end with 2 spaces
                # 3. Next line starts with **
                # 4. Next line is NOT a list item (starting with - or *)
                
                if curr_line.strip() != "":
                    if not curr_line.endswith("  "):
                        if next_line.startswith("**"):
                            # It might be a header if it starts with #
                            # But here we check **
                            # Also check if it's part of a list
                            if not (next_line.startswith("-") or next_line.startswith("* ")):
                                report.write(f"File: {os.path.basename(file_path)}\n")
                                report.write(f"Line {i+1}: {curr_line}\n")
                                report.write(f"Line {i+2}: {lines[i+1].strip()}\n")
                                report.write("-" * 20 + "\n")
                                found_issues = True

    if not found_issues:
        print("No issues found.")
    else:
        print("Issues found. See formatting_issues.txt")

if __name__ == "__main__":
    check_files()
